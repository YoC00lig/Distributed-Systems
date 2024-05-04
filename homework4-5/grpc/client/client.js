import { loadPackageDefinition, credentials } from "@grpc/grpc-js";
import { loadSync } from "@grpc/proto-loader";
import { createInterface } from "readline";
import chalk from "chalk";
import grpc from "@grpc/grpc-js";

const PATH_TO_PROTO_FILE =
  "/Users/joannakulig/Desktop/Distributed-Systems/homework4-5/grpc/protos/shopping.proto";

let eventsServer;
let client;
let calls;
let reader;

const registerCommandHandler = () => {
  reader.on("line", (line) => {
    handleCommand(line);
  });
};

const displayDetailInfo = (detail) => {
  const { product_name, original_price, sale_price, end_time } = detail;
  console.log(chalk.cyan(`Product: ${product_name}`));
  console.log(chalk.magenta(`Original price: ${original_price}`));
  console.log(chalk.red(`Sale price: ${sale_price}`));
  console.log(chalk.gray(`End time: ${new Date(end_time * 1000)}`));
};

const displaySaleInfo = (saleData) => {
  console.log(chalk.bold("\n--------------------"));
  console.log(chalk.blue(`City: ${saleData.city}`));
  console.log(chalk.green(`Type of sale: ${saleData.sale_type}`));
  console.log(chalk.yellow(`Shop name: ${saleData.shop_name}`));
  saleData.details.forEach(displayDetailInfo);
  console.log(chalk.bold("--------------------"));
};

const handleSaleCall = (call, sub) => {
  let bufferedMessages = [];

  call.on("data", (data) => {
    displaySaleInfo(data);
  });
  call.on("end", () => {
    console.log(chalk.gray("Connection end"));
  });
  call.on("error", (error) => {
    if (error.details === "Cancelled on client") {
      return;
    }
    console.error(chalk.red(`Connection error: ${error.message}`));

    call.on("data", (data) => {
      bufferedMessages.push(data);
    });

    if (error.code === grpc.status.INVALID_ARGUMENT) {
      console.error(chalk.yellow("One or more cities do not exist"));
    } else {
      const reconnectInterval = 5000;
      const reconnect = () => {
        setTimeout(() => {
          console.log(chalk.yellow("Attempting to reconnect..."));
          const newCall = client.subscribe(sub);
          handleSaleCall(newCall, sub);
          registerCommandHandler();
        }, reconnectInterval);
      };
      reconnect();
    }
  });
};

const subscribe = (sub) => {
  const call = client.subscribe(sub);
  calls.push(call);
  handleSaleCall(call, sub);
  console.log(chalk.green(`Subscription [${calls.length - 1}]`));
};

const cancelSubscription = (index) => {
  if (index >= 0 && index < calls.length) {
    calls[index].cancel();
    console.log(chalk.red(`Cancelled subscription nr ${index}`));
  } else {
    console.error(chalk.yellow(`Invalid subscription index: ${index}`));
    return;
  }
  calls[index].removeAllListeners("data");
};

const handleCommand = (line) => {
  const args = line.split(" ");
  const command = args.shift();

  const commandFunctions = {
    subscribe: () => {
      const sub = { cities: args };
      subscribe(sub);
    },
    cancel: () => {
      const index = parseInt(args[0]);
      cancelSubscription(index);
    },
    default: () => {
      console.error(chalk.yellow("Given command is invalid!"));
    },
  };

  const selectedFunction =
    commandFunctions[command] || commandFunctions.default;
  selectedFunction();
};

const main = () => {
  const target = process.env.ADDRESS || "localhost:50051";
  try {
    eventsServer = loadPackageDefinition(
      loadSync(PATH_TO_PROTO_FILE, {
        keepCase: true,
        longs: String,
        enums: String,
        defaults: true,
        oneofs: true,
      })
    ).events;

    client = new eventsServer.SaleInformer(
      target,
      credentials.createInsecure(),
      {
        "grpc.keepalive_timeout_ms": 10000,
      }
    );

    calls = [];
    reader = createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    registerCommandHandler();
  } catch (error) {
    console.error(chalk.red(`Error creating gRPC client: ${error.message}`));
    process.exit(1);
  }
};

main();
