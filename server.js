const logger = require('koa-logger');
const serve = require('koa-static');
const koaBody = require('koa-body');
const Router = require('koa-router');
const cors = require('koa2-cors');
const router = new Router({ prefix: '/api' })
const bodyParser = require('koa-bodyparser')
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

const imgStyle = async(ctx)=>{
  try{
    await emotionDetect.test() 
  }catch(err){
    ctx.response.status = err.statusCode || err.status || 500;
    ctx.response.body = {
      message: err.message
    };
  }
}

const getResult = (ctx)=>{
  if(fs.existsSync('happy.png')) {
    console.log('good')
    ctx.body = 'success'
  }else {
    ctx.body = 'failed'
  }
}

router.post('/upload', (ctx)=>{
  ctx.body = 'hello'
})

router.get('/getResult', getResult)

app
  .use(cors())
  .use(logger())
  .use(router.routes())
  .use(router.allowedMethods())
  .use(koaBody({ multipart: true,
    formidable: {
      maxFileSize: 200*1024*1024,	// 设置上传文件大小最大限制，默认2M
      uploadDir: 'upload/',
      onFileBegin: (name, file)=>{	// 文件存储之前对文件进行重命名处理
          file.path = `upload/${file.name}`;
      }
    } 
  }))
  .use(imgStyle)
  .use(servePublicFile)
  .use(download)






// listen
app.listen(3000);
console.log('listening on port 3000');