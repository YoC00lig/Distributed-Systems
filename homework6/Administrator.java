import com.rabbitmq.client.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.concurrent.TimeoutException;

public class Administrator {
    private static final String ADMIN_EXCHANGE = "admin_exchange";
    private static final String ADMIN_QUEUE_NAME = "adminQueue";
    private static final String BROADCAST_EXCHANGE = "broadcast_exchange";

    public static void main(String[] argv) throws IOException, TimeoutException {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");

        try (Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {

            declareExchangeAndQueues(channel);

            Consumer consumer = createConsumer(channel);
            channel.basicConsume(ADMIN_QUEUE_NAME, true, consumer);

            BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));

            String colorCyan = "\u001B[36m";
            String colorReset = "\u001B[0m";

            while (true) {
                System.out.println(colorCyan + "Enter message to broadcast:" + colorReset);
                String input = reader.readLine();
                if ("quit".equals(input)) {
                    break;
                }
                if (!input.startsWith("Message from Administrator:")) {
                    publishMessage(channel, input);
                }
            }
        }
    }

    private static void declareExchangeAndQueues(Channel channel) throws IOException {
        channel.exchangeDeclare(ADMIN_EXCHANGE, BuiltinExchangeType.TOPIC);
        channel.exchangeDeclare(BROADCAST_EXCHANGE, BuiltinExchangeType.FANOUT);
        channel.queueDeclare(ADMIN_QUEUE_NAME, false, false, false, null);
        channel.queueBind(ADMIN_QUEUE_NAME, ADMIN_EXCHANGE, "admin.#");
    }

    private static Consumer createConsumer(Channel channel) {
        return new DefaultConsumer(channel) {
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
                String message = new String(body, StandardCharsets.UTF_8);

                String colorGreen = "\u001B[32m";
                String colorReset = "\u001B[0m";

                if (properties.getHeaders() == null) {
                    System.out.println(colorGreen + " [x] Logged '" + message + "'" + colorReset);
                }
            }
        };
    }

    private static void publishMessage(Channel channel, String input) throws IOException {
        String colorMagenta = "\u001B[35m";
        String colorReset = "\u001B[0m";

        String message = "Message from Administrator: " + input;

        AMQP.BasicProperties props = new AMQP.BasicProperties.Builder()
                .headers(Map.of("sender", "Administrator"))
                .build();

        channel.basicPublish(BROADCAST_EXCHANGE, "", props, message.getBytes(StandardCharsets.UTF_8));
        System.out.println(colorMagenta + " [x] Sent '" + message + "'" + colorReset);
    }
}
