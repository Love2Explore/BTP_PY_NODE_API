# PYTHON Steps
### Steps
  `cf create-service hana hdi-shared pyhana`
  `cf create-service xsuaa application pyuaa -c xs-security.json`
  `cf update-service  pyuaa -c xs-security.json`

  `security File will be used to create xsuaa`

  `{
  "xsappname" : "myapp",
  "tenant-mode" : "dedicated",
  "oauth2-configuration": {
    "redirect-uris": [
        "https://*.cfapps.eu20.hana.ondemand.com/**"
      ]
    }
   }`
  `Add env in manifest.yml`

    `#Refrence - https://developers.sap.com/tutorials/btp-cf-buildpacks-python-create.html`
             `https://developers.sap.com/tutorials/btp-cf-buildpacks-node-create.html`
             `https://blogs.sap.com/2020/07/08/how-to-update-xsuaa-service-instance-to-accept-multiple-redirect-uris/`
# NODEJS Steps