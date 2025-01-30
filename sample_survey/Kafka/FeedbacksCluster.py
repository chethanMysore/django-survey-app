from confluent_kafka import Producer, Consumer
from django.dispatch import Signal
from datetime import datetime
# from sample_survey.signals import incoming_feedback_dispatcher
import os
from asgiref.sync import sync_to_async
import asyncio


class FeedbacksCluster:
    def __init__(self, topic="feedback", group_id="python-group-1", offset_reset="earliest"):
        self.FeedbacksConsumer, self.FeedbacksProducer = None, None
        # sets the consumer group ID and offset
        self.group_id = group_id
        self.offset_reset = offset_reset
        self.config = FeedbacksCluster.read_config(group_id=group_id, offset_reset=offset_reset)
        self.topic = topic
        # creates a new consumer instance
        self.consumer = Consumer(self.config)
        # subscribes to the specified topic
        self.consumer.subscribe([self.topic])
        # creates a new producer instance
        # self.producer = Producer(self.config)

    @staticmethod
    def read_config(group_id, offset_reset):
        # reads the client configuration from client.properties
        # and returns it as a key-value map
        config = {}
        print(os.getcwd())
        with open(f'{os.getcwd()}/sample_survey/configs/client.properties', "r") as fh:
            for line in fh:
                line = line.strip()
                if len(line) != 0 and line[0] != "#":
                    parameter, value = line.strip().split('=', 1)
                    config[parameter] = value.strip()
        # sets the consumer group ID and offset
        config["group.id"] = "python-group-1"
        config["auto.offset.reset"] = "earliest"
        config["enable.auto.commit"] = False
        return config

    # def produce(self, feedbacks=None):
    #     survey_feedbacks = []
    #
    #     if feedbacks:
    #         try:
    #             for feedback in feedbacks:
    #                 key, value = feedback
    #                 survey_feedbacks.append({'key': key, 'value': value})
    #         except Exception as list_parse_error:
    #             print(f'Producer Feedback List Parse Error - {list_parse_error}')
    #             try:
    #                 key, value = feedbacks
    #                 survey_feedbacks.append({'key': key, 'value': value})
    #             except Exception as tuple_parse_error:
    #                 print(f'Producer Feedback Tuple Parse Error - {tuple_parse_error}')
    #
    #     elif feedbacks is None:
    #         survey_feedbacks.append({'key': 'key', 'value': 'value'})
    #
    #     for feedback in survey_feedbacks:
    #         key, value = feedback
    #         self.producer.produce(self.topic, key=key, value=value)
    #         print(f"Produced message to topic {self.topic}: key = {key:12} value = {value:12}")

    def consume_feedbacks(self):
        feedback = None
        try:
            # while True:
            # self.consumer.subscribe([self.topic])
            msg = self.consumer.poll(10.0)
            print(msg)
            if msg:
                msg_error = msg.error()
                if msg_error is not None:
                    print(f'Incoming Message Error - {msg_error}')
                else:
                    msg_key = msg.key().decode("utf-8")
                    msg_val = msg.value().decode("utf-8")
                    msg_created_on = datetime.now()
                    print(f'Incoming Message from cluster - key: {msg_key}, value: {msg_val}, '
                          f'created_on: {msg_created_on}')
                    feedback = {'typ': msg_key, 'msg': msg_val, 'created_on': msg_created_on}
                    # incoming_feedback_dispatcher.send(self.__class__, msg=feedback)
                    # return feedback
        except Exception as e:
            print(f'Error Sending incoming message signal - {e}')
        return feedback

    def flush(self):
        # send any outstanding or buffered messages to the Kafka broker
        self.producer.flush()

    def close(self):
        # closes the consumer connection
        self.consumer.close()


# async def main():
#     print(os.getcwd())
#     # config = read_config()
#     # topic = "feedback"
#     #
#     # # produce(topic, config)
#     # consume(topic, config)
#     feedbacks_cl = FeedbacksCluster(topic='feedback')
#     msg = feedbacks_cl.consume_feedbacks()
#     print(f'msg received - {msg}')
#
#
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
