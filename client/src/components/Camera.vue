<template>
    <div>
      <video id="video" width="500px" height="500px" autoplay="autoplay"></video>
      <canvas id="canvas" width="500px" height="500px"></canvas>
      <!-- <img id="imgTag" src="" alt="imgTag"> -->
      <div>
        <el-button @click="openMedia()">Turn on Camera</el-button>
        <el-button @click="takePhoto()">Capture</el-button>
        <el-button @click="closeMedia()">Turn off Camera</el-button>
      </div>
    </div>
</template>

<script>
    export default {
        name: 'Camera',
        data() {
            return {
                mediaStreamTrack: null,
            }
        },
        methods: {
            openMedia() {
                let constraints = {
                    video: { width: 500, height: 500 },
                    audio: true
                };
                //获得video摄像头
                let video = document.getElementById('video');     
                let promise = navigator.mediaDevices.getUserMedia(constraints);
                promise.then((mediaStream) => {
                    this.mediaStreamTrack = typeof mediaStream.stop === 'function' ? mediaStream : mediaStream.getTracks()[1];
                    video.srcObject = mediaStream;
                    video.play();
                });
            },
            takePhoto() {
                //获得Canvas对象
                let video = document.getElementById('video');
                let canvas = document.getElementById('canvas');
                let ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0, 500, 500);


                // toDataURL  ---  可传入'image/png'---默认, 'image/jpeg'
                let img = document.getElementById('canvas').toDataURL();
                // 这里的img就是得到的图片
                console.log('img-----', img);
                document.getElementById('imgTag').src=img;
            },
            closeMedia() {
                this.mediaStreamTrack.stop();
            },
        }
    }
</script>

<style>
</style>