# CSP and lifecycle patches to vosk-browser 0.0.8

The embedded WebWorker in vosk.js is modified. Upstream copyright notices are retained.

1. createNamedFunction uses a closure and Object.defineProperty instead of Function.
2. craftInvokerFunction uses a generic closure with equivalent argument conversion, destructor execution and return conversion.
3. __emval_get_method_caller uses a generic closure with equivalent pointer reads, method invocation and return conversion.
4. retrieveFinalResult responses include final:true to distinguish an explicit flush from streaming segments.
5. Error responses preserve thrown string messages.
6. Model extraction uses an isolated in-memory filesystem. No IDBFS mount or sync is required. Model parts can be cached normally by the browser.

The app keeps script-src self wasm-unsafe-eval. It does not require unsafe-eval or inline scripts.
