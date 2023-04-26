# import os
# from flask import Flask
# from cfenv import AppEnv
# from hdbcli import dbapi

# app = Flask(__name__)
# env = AppEnv()

# hana_service = 'hana'
# hana = env.get_service(label=hana_service)

# port = int(os.environ.get('PORT', 3000))
# @app.route('/')
# def hello():
#     if hana is None:
#         return "Can't connect to HANA service '{}' – check service name?".format(hana_service)
#     else:
#         conn = dbapi.connect(address=hana.credentials['508d412a-9528-4d3c-8ce1-f409787bc0b9.hna0.prod-eu10.hanacloud.ondemand.com'],
#                              port=int(hana.credentials['443']),
#                              user=hana.credentials['74D975B5E2D242C1B187A25A5B5CCAEF_D5OL8FO6YQT3JPPNEWCL1RFOD_RT'],
#                              password=hana.credentials['Mo4liuzRVkmkGkr.DyperUvBr7BfCjKfAl.xcLWUuMIIHO3zaY0fdrCyk20td5kU32QGdi.R7b70vbAnrEot.xlAWZSgDdnTGs.y3IBa6X-QxZY8RQz.VjHETOmhT7M.'],
#                              encrypt='true',
#                              sslTrustStore=hana.credentials['-----BEGIN CERTIFICATE-----\nMIIDrzCCApegAwIBAgIQCDvgVpBCRrGhdWrJWZHHSjANBgkqhkiG9w0BAQUFADBh\nMQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3\nd3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBD\nQTAeFw0wNjExMTAwMDAwMDBaFw0zMTExMTAwMDAwMDBaMGExCzAJBgNVBAYTAlVT\nMRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j\nb20xIDAeBgNVBAMTF0RpZ2lDZXJ0IEdsb2JhbCBSb290IENBMIIBIjANBgkqhkiG\n9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4jvhEXLeqKTTo1eqUKKPC3eQyaKl7hLOllsB\nCSDMAZOnTjC3U/dDxGkAV53ijSLdhwZAAIEJzs4bg7/fzTtxRuLWZscFs3YnFo97\nnh6Vfe63SKMI2tavegw5BmV/Sl0fvBf4q77uKNd0f3p4mVmFaG5cIzJLv07A6Fpt\n43C/dxC//AH2hdmoRBBYMql1GNXRor5H4idq9Joz+EkIYIvUX7Q6hL+hqkpMfT7P\nT19sdl6gSzeRntwi5m3OFBqOasv+zbMUZBfHWymeMr/y7vrTC0LUq7dBMtoM1O/4\ngdW7jVg/tRvoSSiicNoxBN33shbyTApOB6jtSj1etX+jkMOvJwIDAQABo2MwYTAO\nBgNVHQ8BAf8EBAMCAYYwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUA95QNVbR\nTLtm8KPiGxvDl7I90VUwHwYDVR0jBBgwFoAUA95QNVbRTLtm8KPiGxvDl7I90VUw\nDQYJKoZIhvcNAQEFBQADggEBAMucN6pIExIK+t1EnE9SsPTfrgT1eXkIoyQY/Esr\nhMAtudXH/vTBH1jLuG2cenTnmCmrEbXjcKChzUyImZOMkXDiqw8cvpOp/2PV5Adg\n06O/nVsJ8dWO41P0jmP6P6fbtGbfYmbW0W5BjfIttep3Sp+dWOIrWcBAI+0tKIJF\nPnlUkiaY4IBIqDfv8NZ5YBberOgOzW6sRBc4L0na4UU+Krk2U886UAb3LujEV0ls\nYSEY1QSteDwsOoBrp+uvFRTp2InBuThs4pFsiv9kuXclVzDAGySj4dzp30d8tbQk\nCAUw7C29C79Fv1C5qfPrmAESrciIxpg0X40KPMbp1ZWVbd4=\n-----END CERTIFICATE-----'])

#         cursor = conn.cursor()
#         cursor.execute("select CURRENT_UTCTIMESTAMP from DUMMY")
#         ro = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         return "Current time is: " + str(ro["CURRENT_UTCTIMESTAMP"])

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=port)


import os
from flask import Flask
from cfenv import AppEnv
from flask import request
from flask import abort

from sap import xssec

from hdbcli import dbapi

app = Flask(__name__)
env = AppEnv()

port = int(os.environ.get('PORT', 3000))
hana = env.get_service(label='hana')
uaa_service = env.get_service(name='pyuaa').credentials

@app.route('/')
def hello():
     if 'authorization' not in request.headers:
         abort(403)
     access_token = request.headers.get('authorization')[7:]
     security_context = xssec.create_security_context(access_token, uaa_service)
     isAuthorized = security_context.check_scope('openid')
     if not isAuthorized:
         abort(403)
     return "Hello World!"
    #  conn = dbapi.connect(address=hana.credentials['508d412a-9528-4d3c-8ce1-f409787bc0b9.hna0.prod-eu10.hanacloud.ondemand.com'],
    #                          port=int(hana.credentials['443']),
    #                          user=hana.credentials['74D975B5E2D242C1B187A25A5B5CCAEF_D5OL8FO6YQT3JPPNEWCL1RFOD_RT'],
    #                          password=hana.credentials['Mo4liuzRVkmkGkr.DyperUvBr7BfCjKfAl.xcLWUuMIIHO3zaY0fdrCyk20td5kU32QGdi.R7b70vbAnrEot.xlAWZSgDdnTGs.y3IBa6X-QxZY8RQz.VjHETOmhT7M.'],
    #                          encrypt='true',
    #                          sslTrustStore=hana.credentials['-----BEGIN CERTIFICATE-----\nMIIDrzCCApegAwIBAgIQCDvgVpBCRrGhdWrJWZHHSjANBgkqhkiG9w0BAQUFADBh\nMQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3\nd3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBD\nQTAeFw0wNjExMTAwMDAwMDBaFw0zMTExMTAwMDAwMDBaMGExCzAJBgNVBAYTAlVT\nMRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j\nb20xIDAeBgNVBAMTF0RpZ2lDZXJ0IEdsb2JhbCBSb290IENBMIIBIjANBgkqhkiG\n9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4jvhEXLeqKTTo1eqUKKPC3eQyaKl7hLOllsB\nCSDMAZOnTjC3U/dDxGkAV53ijSLdhwZAAIEJzs4bg7/fzTtxRuLWZscFs3YnFo97\nnh6Vfe63SKMI2tavegw5BmV/Sl0fvBf4q77uKNd0f3p4mVmFaG5cIzJLv07A6Fpt\n43C/dxC//AH2hdmoRBBYMql1GNXRor5H4idq9Joz+EkIYIvUX7Q6hL+hqkpMfT7P\nT19sdl6gSzeRntwi5m3OFBqOasv+zbMUZBfHWymeMr/y7vrTC0LUq7dBMtoM1O/4\ngdW7jVg/tRvoSSiicNoxBN33shbyTApOB6jtSj1etX+jkMOvJwIDAQABo2MwYTAO\nBgNVHQ8BAf8EBAMCAYYwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUA95QNVbR\nTLtm8KPiGxvDl7I90VUwHwYDVR0jBBgwFoAUA95QNVbRTLtm8KPiGxvDl7I90VUw\nDQYJKoZIhvcNAQEFBQADggEBAMucN6pIExIK+t1EnE9SsPTfrgT1eXkIoyQY/Esr\nhMAtudXH/vTBH1jLuG2cenTnmCmrEbXjcKChzUyImZOMkXDiqw8cvpOp/2PV5Adg\n06O/nVsJ8dWO41P0jmP6P6fbtGbfYmbW0W5BjfIttep3Sp+dWOIrWcBAI+0tKIJF\nPnlUkiaY4IBIqDfv8NZ5YBberOgOzW6sRBc4L0na4UU+Krk2U886UAb3LujEV0ls\nYSEY1QSteDwsOoBrp+uvFRTp2InBuThs4pFsiv9kuXclVzDAGySj4dzp30d8tbQk\nCAUw7C29C79Fv1C5qfPrmAESrciIxpg0X40KPMbp1ZWVbd4=\n-----END CERTIFICATE-----'])


    #  cursor = conn.cursor()
    #  cursor.execute("select CURRENT_UTCTIMESTAMP from DUMMY")
    #  ro = cursor.fetchone()
    #  cursor.close()
    #  conn.close()

    #  return "Current time is: " + str(ro["CURRENT_UTCTIMESTAMP"])

@app.route('/post', methods=["POST"])
def post( ):
     if 'authorization' not in request.headers:
         abort(403)
     access_token = request.headers.get('authorization')[7:]
     security_context = xssec.create_security_context(access_token, uaa_service)
     isAuthorized = security_context.check_scope('openid')
     uaa = security_context.check_scope('uaa.user')
     token = security_context.get_app_token()
     if token != access_token:
         abort(400)
     message = request.json['message']
     return {"message": message,"isA": isAuthorized , "uaa":uaa, "token": security_context.get_app_token(), "cli": security_context.get_clientid()  }

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port)