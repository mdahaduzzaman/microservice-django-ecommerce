local typedefs = require "kong.db.schema.typedefs"

return {
  name = "jwt-keycloak",
  fields = {
    { consumer = typedefs.no_consumer },
    { config = {
        type = "record",
        fields = {
          { public_key = { type = "string", required = true }, },
        },
      },
    },
  },
}
