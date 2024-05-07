## Telemetry

LaVague has three possible telemetry modes: `HIGH`, `LOW` and `NONE`

### 📈 Default telemetry

By default, LaVague is set to `LOW` telemetry mode, which records some basic anonymous values to help us improve the product:

- The LLM used
- A randomly generated anonymous session ID
- The URL of the website you used LaVague with
- Whether your action succeeds or fails
- Whether you used the 'launch' or 'build' command

This information helps us monitor the performance of LaVague and what features are most interesting to develop in the future.

## 🚫 Turn off all telemetry

If you want to turn off telemetry, you can set your `TELEMETRY_VAR` environment variable to`NONE`.

### 🤗 Contribute more data

If you would like to help us monitor LaVague further to improve our project, you can set this variable to "HIGH", using the methods listed in the previous section, but switching `NONE` to `HIGH `.

The `HIGH` telemetry option will record the default logged information, plus:

- The code produced by the LLM
- A screenshot of the website before the action runs
- The HTML source code o the website
- The HTML source code chunks sent to the LLM (only the most relevant chunks are sent)
- Your instruction to the LLM