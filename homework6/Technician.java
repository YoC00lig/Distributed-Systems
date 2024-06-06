import com.rabbitmq.client.*;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeoutException;

public class Technician {
    private static final String EXAMS_EXCHANGE = "exams_exchange";
    private static final String RESULTS_EXCHANGE = "results_exchange";
    private static final String ADMIN_EXCHANGE = "admin_exchange";
    private static final String BROADCAST_EXCHANGE = "broadcast_exchange";

    public static final String ANSI_MAGENTA = "\u001B[35m";
    public static final String ANSI_BLUE = "\u001B[34m";
    public static final String ANSI_GREEN = "\u001B[32m";
    public static final String ANSI_RESET = "\u001B[0m";

    public static void main(String[] argv) throws IOException, TimeoutException {
        if (argv.length < 1) {
            System.err.println("Technician type not given");
            System.exit(1);
        }

        int technicianNumber = Integer.parseInt(argv[0]);
        Technician technician = createTechnician(technicianNumber);
        technician.run();
    }

    private static Technician createTechnician(int technicianNumber) {
        String technicianName = (technicianNumber == 1) ? "Technician1" : "Technician2";
        return new Technician(technicianName);
    }

    private final String technicianName;

    public Technician(String technicianName) {
        this.technicianName = technicianName;
    }

    public void run() throws IOException, TimeoutException {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");

        try (Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {

            channel.basicQos(1);
            channel.exchangeDeclare(EXAMS_EXCHANGE, BuiltinExchangeType.TOPIC);
            channel.exchangeDeclare(RESULTS_EXCHANGE, BuiltinExchangeType.TOPIC);
            channel.exchangeDeclare(ADMIN_EXCHANGE, BuiltinExchangeType.TOPIC);
            channel.exchangeDeclare(BROADCAST_EXCHANGE, BuiltinExchangeType.FANOUT);

            System.out.println(ANSI_MAGENTA + this.technicianName + " ready to work!" + ANSI_RESET);

            String kneeQueue = "kneeQueue";
            channel.queueDeclare(kneeQueue, false, false, false, null);
            channel.queueBind(kneeQueue, EXAMS_EXCHANGE, "exam.knee");

            String examType = (technicianName.equals("Technician1")) ? "elbow" : "hip";
            String examQueue = technicianName.toLowerCase() + "_" + examType + "Queue";
            channel.queueDeclare(examQueue, false, false, false, null);
            channel.queueBind(examQueue, EXAMS_EXCHANGE, "exam." + examType);

            Consumer kneeConsumer = createExamConsumer(channel);
            channel.basicConsume(kneeQueue, true, kneeConsumer);

            Consumer examConsumer = createExamConsumer(channel);
            channel.basicConsume(examQueue, true, examConsumer);

            String broadcastQueue = technicianName + "_broadcastQueue";
            channel.queueDeclare(broadcastQueue, false, false, false, null);
            channel.queueBind(broadcastQueue, BROADCAST_EXCHANGE, "");
            channel.basicConsume(broadcastQueue, true, createBroadcastConsumer(channel));

            while (true) {
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        }
    }

    private Consumer createExamConsumer(final Channel channel) {
        return new DefaultConsumer(channel) {
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
                String message = new String(body, StandardCharsets.UTF_8);
                System.out.println(ANSI_BLUE + technicianName + " received '" + message + "'" + ANSI_RESET);

                String result = message + " done";
                String[] routingKeyParts = envelope.getRoutingKey().split("\\.");
                String examType = routingKeyParts[1];
                String doctorName = properties.getHeaders().get("doctorName").toString();

                channel.basicPublish(RESULTS_EXCHANGE, "result." + examType + "." + doctorName, null, result.getBytes(StandardCharsets.UTF_8));
                System.out.println(ANSI_GREEN + technicianName + " sent result: '" + result + "'" + ANSI_RESET);

                sendLogToAdmin(channel, message);
            }
        };
    }

    private void sendLogToAdmin(Channel channel, String message) throws IOException {
        String logMessage = "Log from " + technicianName + ": " + message + " done";
        channel.basicPublish(ADMIN_EXCHANGE, "admin.log", null, logMessage.getBytes(StandardCharsets.UTF_8));
    }

    private Consumer createBroadcastConsumer(final Channel channel) {
        return new DefaultConsumer(channel) {
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
                String message = new String(body, StandardCharsets.UTF_8);
                System.out.println(ANSI_MAGENTA + " [x] " + technicianName + " received broadcast message: '" + message + "'" + ANSI_RESET);
            }
        };
    }
}
