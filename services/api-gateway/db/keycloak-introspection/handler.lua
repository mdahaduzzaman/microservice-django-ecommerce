local http = require("resty.http")
local cjson = require("cjson")

local KeycloakIntrospectionHandler = {
  VERSION  = "1.0.0",
  PRIORITY = 10,
}

function KeycloakIntrospectionHandler:access(config)
    local auth_header = ngx.var.http_authorization

    if not auth_header or not auth_header:find("Bearer ") then
        ngx.log(ngx.ERR, "Missing or invalid Authorization header")
        return ngx.exit(ngx.HTTP_UNAUTHORIZED)
    end

    -- Extract the token
    local access_token = auth_header:match("Bearer%s+(.+)")
    if not access_token then
        ngx.log(ngx.ERR, "Bearer token format invalid")
        return ngx.exit(ngx.HTTP_UNAUTHORIZED)
    end

    local introspection_url = config.keycloak_introspection_url
    --local access_token = ngx.var.http_authorization
    local httpc = http.new()


    local headers = {
        ["Content-Type"] = "application/x-www-form-urlencoded",
    } 

    local body = ngx.encode_args({
        token = access_token,
        client_id = config.client_id,
        client_secret = config.client_secret,
    })

    local request_options = {
        method = "POST",
        body = body,
        headers = headers,
    }

    local res, err = httpc:request_uri(introspection_url, request_options)
    
    ngx.log(ngx.NOTICE, "body ", cjson.encode(request_options))    

    if not res then
        ngx.log(ngx.ERR, "Failed to introspect token: ", err)
        return ngx.exit(ngx.HTTP_INTERNAL_SERVER_ERROR)
    end

    if res.status ~= 200 then
        ngx.log(ngx.ERR, "Token introspection failed with status: ", res.status)
        return ngx.exit(ngx.HTTP_UNAUTHORIZED)
    end

    -- Parse the introspection response
    local introspection_result = cjson.decode(res.body)
    ngx.log(ngx.NOTICE, "Introspection result: ", res.body)

    -- Check if the token is active
    if not introspection_result.active then
        ngx.log(ngx.ERR, "Access token is not active")
        return ngx.exit(ngx.HTTP_UNAUTHORIZED)
    end

    -- Extract roles from realm_access
    local realm_roles = {}
    if introspection_result.realm_access and introspection_result.realm_access.roles then
        for _, role in ipairs(introspection_result.realm_access.roles) do
            table.insert(realm_roles, role)
        end
    end

    -- Extract roles from resource_access
    local resource_roles = {}
    if introspection_result.resource_access then
        for client, access in pairs(introspection_result.resource_access) do
            if access.roles then
                for _, role in ipairs(access.roles) do
                    table.insert(resource_roles, client .. ":" .. role)
                end
            end
        end
    end

    -- Combine and set headers
    ngx.req.set_header("X-Realm-Roles", table.concat(realm_roles, ","))
    ngx.req.set_header("X-Resource-Roles", table.concat(resource_roles, ","))

    -- Add introspection result to request headers
    ngx.req.set_header("X-User-Id", introspection_result.sub)
    ngx.req.set_header("X-Username", introspection_result.username or introspection_result.preferred_username or "")

    ngx.log(ngx.INFO, "Token introspection successful")

    -- Close the HTTP connection
    httpc:close()
end

return KeycloakIntrospectionHandler