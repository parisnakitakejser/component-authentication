# component-authentication

**Project**

- GitHub - profil: https://github.com/parisnakitakejser
- GitHub - Source code: https://github.com/parisnakitakejser/component-authentication

**🌟 Community 🌟**

- Discord: https://discord.gg/6tcWjxV
- Subscribe my channel: https://www.youtube.com/c/ParisNakitaKejser?sub_confirmation=1
- Youtube playlist: https://www.youtube.com/playlist?list=PLLhEJK7fQIxBd-HloE6l6mQ810mcnPV-L
- Donate: https://www.patreon.com/parisnakitakejser


**System environments to set**

| Environment vars        | Fallback                      |
| ----------------------- | ----------------------------- |
| MONGO_DATABASE          | component-authentication      |
| MONGO_HOST              | None                          |
| MONGO_PORT              | None                          |
| MONGO_USERNAME          | None                          |           
| MONGO_PASSWORD          | None                          |
| MONGO_AUTH_SOURCE       | None                          |
| MONGO_MECHANISM         | None                          |
| JWT_TOKEN_SECRET        | None                          |

**Build new images**

If you found eny bugs and want to build your own images, you can do it very quickly by using this command

`docker build -t component-authentication:{version} . --no-cache`

**docker-compose.yaml sample**

    version: "3.7"
    
    services:
        component-authentication:
            image: component-authentication
            ports:
                - "5000:5000"
    
            environment:
                - MONGO_DATABASE=component-authentication
                - MONGO_HOST={hostname}
                - MONGO_PORT={port}
                - MONGO_USERNAME={username}
                - MONGO_PASSWORD={password}
                - MONGO_AUTH_SOURCE=admin
                - MONGO_MECHANISM=SCRAM-SHA-1
                - JWT_TOKEN_SECRET={jwt-secret-token}