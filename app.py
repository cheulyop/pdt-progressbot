import json
import os
from collections import Counter
from datetime import datetime, timedelta, timezone

from firebase_admin import credentials, firestore, initialize_app
from slack_bolt import App


def init_slack_app():
    initialize_app(credentials.Certificate("./credentials/firebase-credentials.json"))

    with open("./credentials/slack-credentials.json", "r") as f:
        creds = json.load(f)

    app = App(token=creds["token"], signing_secret=creds["signing_secret"])

    @app.event("app_mention")
    def get_group_counts(event, say):
        try:
            et = datetime.fromtimestamp(
                float(event["event_ts"]), tz=timezone(timedelta(hours=9))
            )
            counts = Counter(
                map(
                    lambda patient: patient.get().to_dict()["riskGroup"],
                    firestore.client().collection("patients").list_documents(),
                )
            )
            say(
                channel=event["channel"],
                text=f"{et.month:02d}월 {et.day:02d}일 {et.hour:02d}시 {et.minute:02d}분 환자 등록 현황",
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{et.month:02d}월 {et.day:02d}일 {et.hour:02d}시 {et.minute:02d}분 환자 등록 현황*\n>`정상군` {counts['NORMAL_GROUP']}명, `저위험군` {counts['LOW_RISK_GROUP']}명, `고위험군` {counts['HIGH_RISK_GROUP']}명",
                        },
                    },
                ],
            )
        except Exception as e:
            print(e)

    return app


if __name__ == "__main__":
    app = init_slack_app()
    app.start(port=int(os.environ.get("PORT", 3000)))
