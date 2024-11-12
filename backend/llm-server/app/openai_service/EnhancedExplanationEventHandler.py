from aiokafka import AIOKafkaProducer
from openai import AssistantEventHandler

class EnhancedExplanationEventHandler(AssistantEventHandler):
    def __init__(self, thread_id, vector_store, chunk_index=None, kafka_producer=None,
                 kafka_topic="explanation_stream"):
        super().__init__()
        self.thread_id = thread_id
        self.vector_store = vector_store
        self.chunk_index = chunk_index
        self.enhanced_explanation_data = ""
        self.kafka_producer = kafka_producer
        self.kafka_topic = kafka_topic

    async def on_start(self):
        start_message = f"Explanation generation started for chunk {self.chunk_index}."
        await self.kafka_producer.send_and_wait(self.kafka_topic, value=start_message.encode('utf-8'))

    async def on_text_delta(self, delta, snapshot):
        self.enhanced_explanation_data += delta.value
        await self.kafka_producer.send_and_wait(self.kafka_topic, value=delta.value.encode('utf-8'))

    async def on_message_done(self, message):
        complete_message = f"Explanation generation completed for chunk {self.chunk_index}."
        await self.kafka_producer.send_and_wait(self.kafka_topic, value=complete_message.encode('utf-8'))