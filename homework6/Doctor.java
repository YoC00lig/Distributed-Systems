import com.rabbitmq.client.*;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;
import java.util.concurrent.TimeoutException;

public class Doctor {
    private static final String EXAMS_EXCHANGE = "exams_exchange";
    private static final String RESULTS_EXCHANGE = "results_exchange";
    private static final String ADMIN_EXCHANGE = "admin_exchange";
    private static final String BROADCAST_EXCHANGE = "broadcast_exchange";

    public static final String ANSI_BLUE = "\u001B[34m";
    public static final String ANSI_GREEN = "\u001B[32m";
    public static final String ANSI_MAGENTA = "\u001B[35m";
    public static final String ANSI_RESET = "\u001B[0m";

    public static void main(String[] argv) throws IOException, TimeoutException {
        if (argv.length < 1) {
            System.err.println("Doctor name not given.");
            System.exit(1);
        }

        String doctorName = argv[0];
        Doctor doctor = new Doctor(doctorName);
        doctor.run();
    }

    private final String doctorName;
    private final String resultQueue;

    public Doctor(String doctorName) {
        this.doctorName = doctorName;
        this.resultQueue = "resultQueue_" + doctorName;
    }

    public void run() throws IOException, TimeoutException {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");

        try (Connection connection = factory.newConnection();
             Channel channel = connection.createChannel()) {

            channel.exchangeDeclare(EXAMS_EXCHANGE, BuiltinExchangeType.TOPIC);
            channel.exchangeDeclare(RESULTS_EXCHANGE, BuiltinExchangeType.TOPIC);
            channel.exchangeDeclare(ADMIN_EXCHANGE, BuiltinExchangeType.TOPIC);
            channel.exchangeDeclare(BROADCAST_EXCHANGE, BuiltinExchangeType.FANOUT);

            declareAndBindResultQueue(channel);

            String broadcastQueue = doctorName + "_broadcastQueue";
            channel.queueDeclare(broadcastQueue, false, false, false, null);
            channel.queueBind(broadcastQueue, BROADCAST_EXCHANGE, "");

            Thread broadcastThread = new Thread(() -> {
                try {
                    waitForBroadcast(channel, broadcastQueue);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });
            broadcastThread.start();

            Thread resultThread = new Thread(() -> {
                try {
                    waitForResults(channel);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });
            resultThread.start();

            Scanner scanner = new Scanner(System.in);
            while (true) {
                System.out.println(ANSI_BLUE + "Enter patient name:" + ANSI_RESET);
                String patientName = scanner.nextLine();

                System.out.println(ANSI_BLUE + "Enter exam type (e.g., knee):" + ANSI_RESET);
                String examType = scanner.nextLine();

                String message = patientName + " exam for " + examType;
                publishExamMessage(channel, examType, message);

                sendLogToAdmin(channel, message);
            }
        }
    }

    private void publishExamMessage(Channel channel, String examType, String message) throws IOException {
        AMQP.BasicProperties props = new AMQP.BasicProperties.Builder()
                .headers(java.util.Map.of("doctorName", doctorName))
                .build();
        channel.basicPublish(EXAMS_EXCHANGE, "exam." + examType, props, message.getBytes(StandardCharsets.UTF_8));
        System.out.println(ANSI_GREEN + doctorName + " sent '" + message + "'" + ANSI_RESET);
    }

    private void declareAndBindResultQueue(Channel channel) throws IOException {
        channel.queueDeclare(resultQueue, false, false, false, null);
        channel.queueBind(resultQueue, RESULTS_EXCHANGE, "result.#." + doctorName);
    }

    private void sendLogToAdmin(Channel channel, String message) throws IOException {
        String logMessage = "Log from " + doctorName + ": " + message;
        channel.basicPublish(ADMIN_EXCHANGE, "admin.log", null, logMessage.getBytes(StandardCharsets.UTF_8));
    }

    private void waitForBroadcast(Channel channel, String broadcastQueue) throws IOException {
        Consumer consumer = createBroadcastConsumer(channel);
        channel.basicConsume(broadcastQueue, true, consumer);
    }

    private void waitForResults(Channel channel) throws IOException {
        Consumer consumer = createResultConsumer(channel);
        channel.basicConsume(resultQueue, true, consumer);
    }

    private Consumer createBroadcastConsumer(Channel channel) {
        return new DefaultConsumer(channel) {
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
                String message = new String(body, StandardCharsets.UTF_8);
                System.out.println(ANSI_MAGENTA + " [x] " + doctorName + " received broadcast message: '" + message + "'" + ANSI_RESET);
            }
        };
    }

    private Consumer createResultConsumer(Channel channel) {
        return new DefaultConsumer(channel) {
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
                String message = new String(body, StandardCharsets.UTF_8);
                System.out.println(ANSI_GREEN + " [x] " + doctorName + " received result: '" + message + "'" + ANSI_RESET);
            }
        };
    }
}
