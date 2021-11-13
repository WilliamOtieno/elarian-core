import asyncio
from elarian import Elarian, Customer
import requests

org_id = 'el_org_eu_CCi7AV'
app_id = 'el_app_ad5gdI'
api_key = 'el_k_test_9e99b489d41c294d3032488d96ed9e677c624cd12a95814d7299f5ba8eec0745'

url = "http://127.0.0.1:8000/start/"
print(url)

client = Elarian(org_id=org_id, app_id=app_id, api_key=api_key)

sms_channel = {
    'number': '75923',
    'channel': 'sms'
}

message = {
    'body': {'text': 'Your tax returns have been filed successfully.'}
}


async def handleUSSD(notif, customer, app_data, callback):
    customer = Customer(client=client, number="+254719383956", provider="cellular")
    print('USSD has been triggered')

    menu = {
        "text": "Welcome. Please enter your KRA PIN to trigger the process",
        "is_terminal": False
    }
    user_input = notif["input"]["text"]
    if user_input == '':
        menu = {
            "text": "Welcome. Please enter your KRA PIN to trigger the process",
            "is_terminal": False
        }
    else:
        menu = {
            "text": "Thank you, your request has been received.",
            "is_terminal": True
        }
        await customer.send_message(messaging_channel=sms_channel, message=message)
        payload = {'pin': f'{notif["input"]["text"]}'}
        response = requests.request("POST", url, data=payload)

    callback({'body': {'ussd': menu}}, {'screen2': 'end'})


async def on_connected():
    will = Customer(client=client, number="+254719383956", provider="cellular")
    print("Running!")
    data = {
        "name": "William",
    }
    await will.update_metadata(data)
    resp = await will.get_state()


async def start():
    client.set_on_connection_error(lambda err: print(f"Connection Error: {err}"))
    client.set_on_connected(on_connected)
    client.set_on_ussd_session(handleUSSD)
    await client.connect()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    loop.run_forever()
