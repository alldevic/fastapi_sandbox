"use strict";

const OpenAPISnippet = require("openapi-snippet");
const router = require("@koa/router")();
const koaBody = require("koa-body").default;
const Koa = require("koa");
const app = (module.exports = new Koa());

function enrichSchema(schema, targets) {
  for (var path in schema.paths) {
    for (var method in schema.paths[path]) {
      var generatedCode = OpenAPISnippet.getEndpointSnippets(
        schema,
        path,
        method,
        targets
      );
      schema.paths[path][method]["x-codeSamples"] = [];
      for (var snippetIdx in generatedCode.snippets) {
        const snippet = generatedCode.snippets[snippetIdx];
        var lang = snippet.id.split("_")[0]
        const source = snippet.content.replaceAll('%7B','{').replaceAll('%7D','}')

        schema.paths[path][method]["x-codeSamples"][snippetIdx] = {
          lang: lang,
          label: snippet.title,
          source: source,
        };
      }
    }
  }
  return schema;
}

router.post("/enrich", koaBody({ json: true }), (ctx) => {
  const body = ctx.request.body;
  const result = enrichSchema(body.schema, body.targets);
  ctx.body = result;
});


// logger
app.use(async (ctx, next) => {
  console.log(`${new Date().toISOString()} -->> ${ctx.method} ${ctx.url}`)
  await next();
  const rt = ctx.response.get("X-Response-Time");
  console.log(`${new Date().toISOString()} <<-- ${ctx.method} ${ctx.url} - ${rt}`);
});

// x-response-time
app.use(async (ctx, next) => {
  const start = Date.now();
  await next();
  const ms = Date.now() - start;
  ctx.set("X-Response-Time", `${ms}ms`);
});

// routes
app.use(router.routes()).use(router.allowedMethods());

app.listen(3000);
console.log("started at 3000")
