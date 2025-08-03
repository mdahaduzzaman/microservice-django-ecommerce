FROM kong/kong-gateway:3.10.0.2

USER root

# Install required Lua modules
RUN apk add --no-cache git curl unzip \
  && luarocks install lua-resty-openidc \
  && luarocks install lua-resty-session \
  && luarocks install luacrypto || true

USER kong
