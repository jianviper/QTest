/**
 * Created by J on 2018/12/8.
 */

$(window).load(function () {
    checkLogin();
    checkOpenid();
    //适当延迟隐藏，提高loading效果
    $('#loading').delay(618).hide(0);
    //$('#loading').hide(0);
    $('#floatLayerid').delay(618).hide(0);
});

//检查是否需要登录
function checkLogin() {
    let check = $("input:checkbox[name='check_login']:checked").val();
    $('.form-group:eq(8)').hide();//加密密码
    if (check) {
        // $("#slt").show();
        let site = $('#site');
        $('.form-group:eq(2)').hide();//公司
        $('.form-group:eq(5)').hide();//仓库
        $('.form-group:eq(6)').hide();//仓库ID
        if (site.prop('selectedIndex') > 1 && site.prop('selectedIndex') < 6) {//门店APP，进销存
            // getStock();
            $('.form-group:eq(5)').show();
            $('.form-group:eq(6)').show();
        }
        else if (site.prop('selectedIndex') > 7) {//SGMW
            $('.form-group:eq(2)').show();
        }
        $('.form-group:eq(3)').show();//用户名
        $('.form-group:eq(4)').show();//密码
        $("#checklogin").attr("value", "checked");
    }
    else {
        $("#check_login").attr("value", "unchecked");
        $('.form-group:eq(2)').hide();
        $('.form-group:eq(3)').hide();
        $('.form-group:eq(4)').hide();
        $('.form-group:eq(5)').hide();
        $('.form-group:eq(6)').hide();
    }
}

function checkOpenid() {
    let check = $("input:checkbox[name='check_openid']:checked").val();
    if (check) {
        $('.form-group:eq(7)').show();
    }
    else {
        $("#check_openid").attr("value", "unchecked");
        $('.form-group:eq(7)').hide();
    }
}

function checkUser() {
    let site = $('#site');
    let api_name = $("#api_name").val().trim();
    let post_data = $("#api_data").val().trim();
    let check = $("input:checkbox[name='check_login']:checked").val();
    let randimg = parseInt(10 * Math.random() + 1);
    $("#loading_img").attr('src', 'static/img/' + String(randimg) + '.gif');
    if (!api_name) {
        return false;
    }
    else if (check && (site.prop('selectedIndex') === 4 || site.prop('selectedIndex') === 5) && $('#stock_name').val() === "") {
        $('#stock_name').focus();
        return false;
    }
    else if (check && ($("#username").val() === "" || $("#password").val() === "")) {
        $("#username").focus();
        return false;
    }
    $('#loading').show();
    $('#floatLayerid').show();
    $('.form-group:eq(3)').val(null);
    storage = window.localStorage;
    if (storage.length === 0) {
        storage.setItem(api_name, post_data)
    }
    else {
        for (i = 0; i < storage.length; i++) {
            if (storage.key(i) === api_name) {
                storage.setItem(api_name, post_data);
                return true;
            }
        }
        storage.setItem(api_name, post_data);
    }
}

function inputData() {
    let api_name = $("#api_name").val().trim();
    storage = window.localStorage;
    if (storage.length === 0) {
        return true;
    }
    else {
        for (i = 0; i < storage.length; i++) {
            if (storage.key(i) === api_name) {
                $("#api_data").val(storage.getItem(api_name));
                return true;
            }
        }
    }
}

function clearData() {
    $("#reponse_data").val('');
}

function getStock() {
    let site = $('#site');
    //console.log('site:' + site.val());
    if (site.prop('selectedIndex') > 1 && site.prop('selectedIndex') < 6) {
        let stock = $('#stock_list');
        let username = $('#username').val();
        stock.empty();
        // stock.append("<option value='0'>请选择仓库</option>");
        if (username) {
            let stock_val = '';
            $.post('getStocks', {'username': username, 'site': site.val()}, function (result) {
                //console.log(result);
                for (i = 0; i < result.length; i++) {
                    //stock.append("<option value=" + result[i]['stock_id'] + '|' + result[i]['stock_name'] + ">" + result[i]['stock_name'] + "</option>");
                    stock_val = stock_val + result[i]['stock_id'] + ' | ' + result[i]['stock_name'] + '\r\n';
                }
                stock.val(stock_val);
            });
        }
    }
}

function encrypt() {
    let site = $('#site');
    let password = $('#password');
    if (password.val() && site.prop('selectedIndex') < 8) {//仅企商汇和修车仔密码加密
        let pwd = $('#pwd');
        let keystr = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCIyirbChVxQFk3n5ZDyBksvMEmdDIWM+52iGIgItINV0ivasC2MpE1OzFzwgLt2nv14LXJTRmawLf1cduRhVWT13ldhidL601KE23Wabo30TKNJmMR0gLPD2PTq5JjmuwxSEd5AIdGm3OIaRrScQ24PlEbho2+ApTLjzCknGkY1wIDAQAB';
        let encrypt = new JSEncrypt();
        encrypt.setPublicKey(keystr);
        pwd.val(encrypt.encrypt(password.val()));
    }
}