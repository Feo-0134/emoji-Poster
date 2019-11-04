var exec = require('child_process').exec;
const fs = require('fs');

//先发第一个环节码100，等待返回正确数据再进行发送下一个码
// component.execCmd();

//该方法用于命令行执行python命令 类似于:  python py_test.py arg1
//这样在python中就可以接受传递过去的参数
function sleep(milliSeconds) {
    var startTime = new Date().getTime();
    while (new Date().getTime() < startTime + milliSeconds);
}

const test = (fileName) => {
    exec('python main.py ' + fileName, function (error, stdout, stderr) {
        if(error){
            console.error('error: ' + error);
            return;
        }
    })
}

const testObj = {
    test: test
}

module.exports = testObj