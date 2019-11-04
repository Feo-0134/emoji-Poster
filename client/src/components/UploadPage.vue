<template>
<el-container class="hello">
  <el-header class="appTitle">
  <div class="titleBox Box1">
    <img class="iconImg" alt="Vue logo" src="../assets/logo.png">
  </div>
  <div class="titleBox">
    <p>{{ msg }}</p>
  </div>
  </el-header>
  <el-main class = "mainContent">
    <div v-if="showPost == true">
      <el-row class = "marginTop60" v-if="happy">
        <el-col>
          <el-card class="postCard" :body-style="{ padding: '0px' }">
            <img src="../assets/img4.png" class="image">
            <div style="padding: 14px;">
              <span>Fresh Post</span>
              <div class="bottom clearfix">
                <el-button type="text" class="button">Read More</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
        </el-row>
        <el-row class = "marginTop60" v-if="!happy">
        <el-col>
          <el-card class="postCard" :body-style="{ padding: '0px' }">
            <img src="../assets/img5.jpg" class="image">
            <div style="padding: 14px;">
              <span>Fresh Post</span>
              <div class="bottom clearfix">
                <el-button type="text" class="button">Read More</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
        </el-row>
        <el-row class = "marginTop60" v-if="false">
        <el-col>
          <el-card class="postCard" :body-style="{ padding: '0px' }">
            <img src="../assets/img6.jpeg" class="image">
            <div style="padding: 14px;">
              <span>Fresh Post</span>
              <div class="bottom clearfix">
                <el-button type="text" class="button">Read More</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    <div>
    <el-upload
      class="upload-demo"
      action="http://localhost:3000/api/upload"
      :on-preview="handlePreview"
      :on-remove="handleRemove"
      :before-remove="beforeRemove"
      multiple
      :limit="3"
      :on-exceed="handleExceed"
      :file-list="fileList">
      <el-button class="titleBox">Capture</el-button>
    </el-upload>
    <el-button class="titleBox" @click="showPost = true;getResult()">
    <el-link :underline="false" href="javascript:;">Get Post</el-link>
    </el-button>
    </div>
    <Camera v-show="showCamera"/>
  </el-main>
  <el-footer>a piece of blur code</el-footer>
</el-container>
</template>

<script>
import Camera from './Camera.vue'
  export default {
    name: 'UploadPage',
    components: {
      Camera
    },
    props: {
      msg: String,
    },
    data(){
      return {
        currentDate: new Date(),
        file:"",
        message:"",
        fileList: [],
        showPost: false,
        showCamera: false,
        happy: false,
      }
    },
    methods: {
      // templateFunc() {
      //   this.$http.get(this.downloadApiPath)
      //   .then((response)=> {
      //     console.log(response)
      //   })
      //   .catch((error)=>{
      //       console.log(error)
      //   })
      // },
      downloadFile() {
        window.location.href = this.downloadApiPath
      },
      handleRemove(file, fileList) {
        console.log(file, fileList);
      },
      handlePreview(file) {
        console.log(file);
      },
      handleExceed(files, fileList) {
        this.$message.warning(`The limit is 3, you selected ${files.length} files this time, add up to ${files.length + fileList.length} totally`);
      },
      beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${ file.name }？`);
      },
      getResult() {        
        return new Promise((resolve, reject)=>{
          this.$http.get('http://localhost:3000/api/getResult')
          .then((response)=> {
            console.log(response)
            if(response.data === 'success'){
              this.happy = true
            }else {
              this.happy = false
            }
          })
        })
      }
    },
    computed:{
      downloadApiPath() {
        return (
          'http://localhost:3000/public/temp.zip'
        );
      },
      uploadApiPath() {
        return (
          'http://localhost:3000/api/upload'
        );
      },
      uploadApiPayload() {
        return {
          files:{
            file:{
              path:this.$refs.file.files[0].path,
              name:'helloWorld.txt'
            }
          }
        }
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .el-col-8 {
    width: 65% !important;
    margin: auto !important;

  }
  .postCard {
    margin: auto;
    width: 50%;
  }
  .marginTop60 {
    margin-top: 60px;
  }
  .mainContent {
    min-height: 350px;
    margin-top: 100px;
  }
  h3 {
    margin: 40px 0 0;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    display: inline-block;
    margin: 0 10px;
  }
  a {
    color: #42b983;
  }
  .appTitle {
    text-align: left !important;
  }
  .iconImg {
    height: 50px;
    width: 50px !important;
  }
  .titleBox {
    height: 50px;
    display: inline-block;
    width: 200px;
    margin: 10px;
  }
  .Box1 {
    width: 70px !important;
  }
    .time {
    font-size: 13px;
    color: #999;
  }
  
  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    padding: 0;
    float: right;
  }

  .image {
    width: 100%;
    display: block;
  }

  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }
  
  .clearfix:after {
      clear: both
  }
</style>
