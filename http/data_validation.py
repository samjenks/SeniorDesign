import os
import json

tags = ['AccessTime', 'Identifier', 'AccessArea', 'AddTime', 'AddTimeUnit']

def receive_data(data):
    processed = data #json.parse(data)
    intents = processed['request']['intent']

    with open('data.json', 'w') as outfile:
        output = {}
        output[intents['slots']['Identifier']['value']] = {'AccessTime': intents['slots']['AccessTime'],
                                                           'AccessArea': intents['slots']['AccessTime']}

        json.dump(output, outfile)


def test_validity(data_file):
    json_data = open(data_file).read()

    data = json.loads(json_data)
    for key in data:
        log = data[key]
        if (tag in log for tag in tags):
            return True
        else:
            return False



if __name__ == '__main__':
    temp_data = {
        "version": "1.0",
        "session": {
            "new": True,
            "sessionId": "amzn1.echo-api.session.c7fc5852-b315-4955-a352-c2011ee852e4",
            "application": {
                "applicationId": "amzn1.ask.skill.ad7a0fe1-278c-47e7-a664-6564e986c41e"
            },
            "user": {
                "userId": "amzn1.ask.account.AGVTPEH5GY2EFH6Q5QZHMQ36VEVOTJLXVPMX4FYY4BSYJW746ROJBQZQVNAVVXUS3PR34VXXSA72FQPL72MM4QCEEMIDKO6UKGBEALU7F2RT76MFT5GGIA5FYXBWDUETWJLSAYC7H6HAZM5VBGWXWA32DBA7IAB7UTGQ2IY65IPSFCB2CWXCY2UC4TKP6GH2PWCEWKL24Z6EQII"
            }
        },
        "context": {
            "AudioPlayer": {
                "playerActivity": "IDLE"
            },
            "Display": {},
            "System": {
                "application": {
                    "applicationId": "amzn1.ask.skill.ad7a0fe1-278c-47e7-a664-6564e986c41e"
                },
                "user": {
                    "userId": "amzn1.ask.account.AGVTPEH5GY2EFH6Q5QZHMQ36VEVOTJLXVPMX4FYY4BSYJW746ROJBQZQVNAVVXUS3PR34VXXSA72FQPL72MM4QCEEMIDKO6UKGBEALU7F2RT76MFT5GGIA5FYXBWDUETWJLSAYC7H6HAZM5VBGWXWA32DBA7IAB7UTGQ2IY65IPSFCB2CWXCY2UC4TKP6GH2PWCEWKL24Z6EQII"
                },
                "device": {
                    "deviceId": "amzn1.ask.device.AGYWS2T3LMBTGW22MIXXUQHTEACGPF6BZMI634SNEQNXDAHUIZZLOIEYIAKVRV4T33MTAGTVUWY5NRJCTVTP2SN2CTRJWBOZALDXXCGLK7POMUBNUB6XCQRMUWAU7SXJDOD7PEC456Z6QC74GFARUFXOBJYOIMOLM6X2DG7GR53S4K6IWTQF2",
                    "supportedInterfaces": {
                        "AudioPlayer": {},
                        "Display": {
                            "templateVersion": "1.0",
                            "markupVersion": "1.0"
                        }
                    }
                },
                "apiEndpoint": "https://api.amazonalexa.com",
                "apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLmFkN2EwZmUxLTI3OGMtNDdlNy1hNjY0LTY1NjRlOTg2YzQxZSIsImV4cCI6MTUzOTM3Mjc1OCwiaWF0IjoxNTM5MzY5MTU4LCJuYmYiOjE1MzkzNjkxNTgsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUdZV1MyVDNMTUJUR1cyMk1JWFhVUUhURUFDR1BGNkJaTUk2MzRTTkVRTlhEQUhVSVpaTE9JRVlJQUtWUlY0VDMzTVRBR1RWVVdZNU5SSkNUVlRQMlNOMkNUUkpXQk9aQUxEWFhDR0xLN1BPTVVCTlVCNlhDUVJNVVdBVTdTWEpET0Q3UEVDNDU2WjZRQzc0R0ZBUlVGWE9CSllPSU1PTE02WDJERzdHUjUzUzRLNklXVFFGMiIsInVzZXJJZCI6ImFtem4xLmFzay5hY2NvdW50LkFHVlRQRUg1R1kyRUZINlE1UVpITVEzNlZFVk9USkxYVlBNWDRGWVk0QlNZSlc3NDZST0pCUVpRVk5BVlZYVVMzUFIzNFZYWFNBNzJGUVBMNzJNTTRRQ0VFTUlES082VUtHQkVBTFU3RjJSVDc2TUZUNUdHSUE1RllYQldEVUVUV0pMU0FZQzdINkhBWk01VkJHV1hXQTMyREJBN0lBQjdVVEdRMklZNjVJUFNGQ0IyQ1dYQ1kyVUM0VEtQNkdIMlBXQ0VXS0wyNFo2RVFJSSJ9fQ.iX0VTjnB6W0YBfPS7o9dp7wftSliYxwFoiMIsMEtgioqw54fNg_RWi1a4QOklhXoVEyMMIibnEGAgBf5sbQZ9zfhsG2qoPjFU5sS2WAB7E9HcMbRei0F3UsrYZ-RFcDfWSjOm688GBHnHy7NqDJ5pWS2ClPAx3bZIaba3MqLsyWF65_TNPs8LZegXpLM5mtOoKLoOZu-QC2rDaRhlJlUy3iky8Dki06TPVjagLE6RYfWFSDlSvdbuWtglT_oSPej66Q5KKUvze5nGeQVzwFfT4NibjxNkutV0xISiFIa_imj5mA-wNF7_NeTX4-RS-W48-nc-NdC16b-ZVq2ztgq_g"
            }
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "amzn1.echo-api.request.cd870161-f374-4003-8f4d-764e37b5de64",
            "timestamp": "2018-10-12T18:32:38Z",
            "locale": "en-US",
            "intent": {
                "name": "GiveAccess",
                "confirmationStatus": "NONE",
                "slots": {
                    "AccessTime": {
                        "name": "AccessTime",
                        "value": "17:32",
                        "confirmationStatus": "NONE",
                        "source": "USER"
                    },
                    "Identifier": {
                        "name": "Identifier",
                        "value": "user1",
                        "confirmationStatus": "NONE",
                        "source": "USER"
                    },
                    "AccessArea": {
                        "name": "AccessArea",
                        "value": "area1",
                        "confirmationStatus": "NONE",
                        "source": "USER"
                    }
                }
            }
        }
    }
    receive_data(temp_data)
    #print(test_validity('data.json'))


