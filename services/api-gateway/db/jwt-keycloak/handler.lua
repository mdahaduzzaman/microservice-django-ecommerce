local jwt = require "resty.jwt"
local cjson = require "cjson"
local http = require "resty.http"

local kong = kong

local plugin = {
  PRIORITY = 1000,
  VERSION = "1.0.0",
}

function plugin:access(config)
  -- Step 1: Get Authorization header
  local auth_header = kong.request.get_header("authorization")
  if not auth_header then
    kong.log.warn("[jwt-keycloak] Missing Authorization header")
    return kong.response.exit(401, { message = "Missing Authorization header" })
  end

  -- Step 2: Extract Bearer token
  local _, _, token = string.find(auth_header, "Bearer%s+(.+)")
  if not token then
    kong.log.warn("[jwt-keycloak] Invalid Authorization header format")
    return kong.response.exit(401, { message = "Invalid Authorization header format" })
  end

  local public_key_pem = "-----BEGIN PUBLIC KEY-----\n" ..
                          config.public_key .. "\n" ..
                          "-----END PUBLIC KEY-----"

  -- Step 6: Verify token signature
  local verified = jwt:verify(public_key_pem, token)

  if not verified.verified then
    kong.log.warn("[jwt-keycloak] JWT verification failed: ", verified.reason or "unknown reason")
    return kong.response.exit(401, { message = "Invalid or expired token" })
  end

  -- Extract roles from realm_access
  local realm_roles = {}
  if verified.payload.realm_access and verified.payload.realm_access.roles then
      for _, role in ipairs(verified.payload.realm_access.roles) do
          table.insert(realm_roles, role)
      end
  end

  -- Extract roles from resource_access
  local resource_roles = {}
  if verified.payload.resource_access then
      for client, access in pairs(verified.payload.resource_access) do
          if access.roles then
              for _, role in ipairs(access.roles) do
                  table.insert(resource_roles, client .. ":" .. role)
              end
          end
      end
  end

  kong.log.warn("[jwt-keycloak] JWT verified successfully for sub: ", verified.payload.sub or "unknown")

  -- Combine and set headers
  ngx.req.set_header("X-Realm-Roles", table.concat(realm_roles, ","))
  ngx.req.set_header("X-Resource-Roles", table.concat(resource_roles, ","))

  -- Step 7: (Optional) Inject user warn headers to upstream
  kong.service.request.set_header("X-User-Id", verified.payload.sub or "")
  kong.service.request.set_header("X-User-Email", verified.payload.email or "")
end

return plugin
