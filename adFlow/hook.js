



function parse_data(data, stack, pkgname){
    if (isAD(data, stack, pkgname)){

    }
    else{

    }
}

function sendAD(sdk, data, stack, pkgname){
    var packet = {
        'sdk': sdk,
        'data': data,
        'stack': stack,
        'pkgname': pkgname
    };
    send("flow:::" + JSON.stringify(packet));
}

function isAD(data, stack, pkgname){
    if (stack.indexOf("com.qq") != -1 /*&& data.indexOf("txt") != -1 && data.indexOf("last_ads") != -1*/){
        sendAD("广点通", data, stack, pkgname);
        return true;
    }
    
    if (stack.indexOf("com.bytedance") != -1 /*&& data.indexOf("title") != -1 && data.indexOf("filter_words") != -1*/){ 
        sendAD("穿山甲", data, stack, pkgname);
        return true;
    }
    
    if (stack.indexOf("com.kwad") != -1 /*&& data.indexOf("adDescription") != -1 && data.indexOf("downloadSafeInfo") != -1*/){
        sendAD("快手", data, stack, pkgname);
        return true;
    }
    
    if (data.indexOf("passback") != -1 && data.indexOf("materiallogsdk.tt.cn") != -1){
        sendAD("新萌", data, stack, pkgname);
        return true;
    }

    if (stack.indexOf("baidu") != -1 ){
        send("百度", data, stack, pkgname);
        return true;
    }

    if (data.indexOf("tuifish.com") != -1){
        send("推啊", data, stack, pkgname);
        return true;
    }

    if (data.indexOf("qutoutiao.net") != -1){
        send("趣头条", data, stack, pkgname);
        return true;
    }

    if (data.indexOf("etouch.cn") != -1){
        send("微鲤", data, stack, pkgname);
        return true;
    }
    return false;
}

function regist(pkgname){
    Java.perform(function(){
        console.log("in perform ......");
        var ClassName = "org.json.JSONObject";
        var Platform = Java.use(ClassName);
        var targetMethod = "$init";
        var len = Platform[targetMethod].overloads.length;   //重载个数
        for(var i = 0; i < len; ++i) {
            Platform[targetMethod].overloads[i].implementation = function () {    //hook所有的重载
                var stackstr = Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new());
                for (var j = 0; j < arguments.length; j++) {
                    parse_data(arguments[j], stackstr, pkgname)
                }   
                this[targetMethod].apply(this, arguments);
            }
        }      
    })
}

rpc.exports = {
    initjs: function initjs(pkgname) {
        regist(pkgname);
        return;
    }
};