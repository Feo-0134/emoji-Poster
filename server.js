const logger = require('koa-logger');
const serve = require('koa-static');
const koaBody = require('koa-body');
const Router = require('koa-router');
const cors = require('koa2-cors');
const router = new Router({ prefix: '/api' })
const Koa = require('koa');
const fs = require('fs');
const app = new Koa();
const os = require('os');
const path = require('path');
const extname = path.extname;
const URL = require('url');
var multer = require("multer");
var upload = multer({dest:'./upload'});

const emotionDetect = require('./cmd2Py')

// serve files from ./public
const servePublicFile = serve(path.join(__dirname, '/public'))


// handle uploads
const uploadFile = async function (ctx) {
  var result = emotionDetect()
  // const file = ctx.request.body.file;	// 获取上传文件
	// const reader = fs.createReadStream(file.path);	// 创建可读流
	// const upStream = fs.createWriteStream(`upload/${file.name}`);		// 创建可写流
  // reader.pipe(upStream);	// 可读流通过管道写入可写流
  console.log(result)
	return ctx.body = 'nature';
}

function stat(file) {
  return new Promise(function(resolve, reject) {
    fs.stat(file, function(err, stat) {
      if (err) {
        reject(err);
      } else {
        resolve(stat);
      }
    });
  });
}

const download = async function(ctx) {
  console.log(ctx.path)
  const fpath = path.join(__dirname, ctx.path);
  const fstat = await stat(fpath);

  if (fstat.isFile()) {
    console.log('isFile')
    ctx.type = extname(fpath);
    ctx.body = fs.createReadStream(fpath);
  }
}

router.post('/upload', uploadFile)

app.use(cors({
  origin: function (ctx) {
      if (ctx.url === '/test') {
          return "*"; // 允许来自所有域名请求
      }
      return 'http://localhost:8080'; // 这样就能只允许 http://localhost:8080 这个域名的请求了
  },
  exposeHeaders: ['WWW-Authenticate', 'Server-Authorization'],
  maxAge: 5,
  credentials: true,
  allowMethods: ['GET', 'POST', 'DELETE'],
  allowHeaders: ['Content-Type', 'Authorization', 'Accept'],
}))

app
  .use(logger())
  .use(koaBody({ multipart: true,
    formidable: {
      maxFileSize: 200*1024*1024,	// 设置上传文件大小最大限制，默认2M
      uploadDir: 'upload/',
      onFileBegin: (name, file)=>{	// 文件存储之前对文件进行重命名处理
          file.path = `upload/${file.name}`;
      }
    } 
  }))
  .use(servePublicFile)
  .use(router.allowedMethods())
  .use(router.routes())
  .use(download)



// listen
app.listen(3000);
console.log('listening on port 3000');