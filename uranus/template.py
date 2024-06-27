import http.client
import json


def domain_test_template():
    body = '''<div>
    <includetail>
        <div style="font:Verdana normal 14px;color:#000;">
            <div style="position:relative;">
                <div class="eml-w eml-w-sys-layout">
                    <div style="font-size: 0px;">
                        <div class="eml-w-sys-line">
                            <div class="eml-w-sys-line-left"></div>
                            <div class="eml-w-sys-line-right"></div>
                        </div>
                        <div class="eml-w-sys-logo" style="float: right">
                            <img src="data:image/png;base64,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" alt=""/>
                        </div>
                    </div>
                    <div class="eml-w-sys-content">
                        <div class="dragArea gen-group-list">
                            <div class="gen-item">
                                <div class="eml-w-item-block" style="padding: 0px;">
                                    <div class="eml-w-title-level1">域名测试通知</div>
                                </div>
                            </div>
                            <div class="gen-item" draggable="false" style="margin-top: 16px;">
                                <hr color="#E9E9E9" size="1"/>
                                <div class="eml-w-item-block" style="padding: 0px 0px 0px 1px;">
                                    <div class="eml-w-title-level3">
                                        <span>{{index . "project"}}项目{{index . "iteration"}}版本已经归档。信息如下：</span>
                                        <div style="margin-top: 16px;">
                                            <table style="font-size: 14px;">
                                                <tr>
                                                    <td style="font-weight: 500">域名：</td>
                                                    <td style="color: blue;">{{index . "domain"}}</td>
                                                </tr>
                                                <tr>
                                                    <td style="font-weight: 500">产品经理：</td>
                                                    <td style="color: blue;">{{index . "projectManager"}}</td>
                                                </tr>
                                                <tr>
                                                    <td style="font-weight: 500">项目管理员：</td>
                                                    <td style="color: blue;">{{index . "projectOwner"}}</td>
                                                </tr>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="eml-w-sys-footer">BeeCloud APIKEY</div>
                </div>
            </div>
        </div><!--<![endif]-->
    </includetail>
</div>

<style>
    .eml-w-title-level1 {
        font-size: 20px;
        font-weight: 500;
        padding: 15px 0
    }

    .eml-w-title-level3 {
        font-size: 14px;
        font-weight: 500;
        padding-bottom: 10px
    }

    .eml-w-sys-layout {
        background: #fff;
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, .2);
        border-radius: 4px;
        margin: 50px auto;
        max-width: 800px;
        overflow: hidden
    }

    .eml-w-sys-line-left {
        display: inline-block;
        width: 88%;
        background: #0887FF;
        height: 3px
    }

    .eml-w-sys-line-right {
        display: inline-block;
        width: 11.5%;
        height: 3px;
        background: #0887FF;
        opacity: 0.7;
        margin-left: 1px
    }

    .eml-w-sys-logo {
        text-align: right
    }

    .eml-w-sys-logo img {
        display: inline-block;
        margin: 30px 50px 0 0
    }

    .eml-w-sys-content {
        position: relative;
        padding: 20px 50px 0;
        min-height: 216px;
        word-break: break-all
    }

    .eml-w-sys-footer {
        font-weight: 500;
        font-size: 12px;
        color: #bebebe;
        letter-spacing: .5px;
        padding: 0 0 30px 50px;
        margin-top: 60px
    }

    .eml-w {
        font-family: Helvetica Neue, Arial, PingFang SC, Hiragino Sans GB, STHeiti, Microsoft YaHei, sans-serif;
        -webkit-font-smoothing: antialiased;
        color: #2b2b2b;
        font-size: 14px;
        line-height: 1.75
    }

    .eml-w a {
        text-decoration: none
    }

    .eml-w a, .eml-w a:active {
        color: #186fd5
    }

    .eml-w h1, .eml-w h2, .eml-w h3, .eml-w h4, .eml-w h5, .eml-w h6, .eml-w li, .eml-w p, .eml-w ul {
        margin: 0;
        padding: 0
    }

    .eml-w-item-block {
        margin-bottom: 10px
    }

    @media (max-width: 420px) {
        .eml-w-sys-layout {
            border-radius: none !important;
            box-shadow: none !important;
            margin: 0 !important
        }

        .eml-w-sys-layout .eml-w-sys-line {
            display: none
        }

        .eml-w-sys-layout .eml-w-sys-logo img {
            margin-right: 30px !important
        }

        .eml-w-sys-layout .eml-w-sys-content {
            padding: 0 35px !important
        }

        .eml-w-sys-layout .eml-w-sys-footer {
            padding-left: 30px !important
        }
    }
    table tr td:first-child {
        width: 100px
    }
    table {
        font-size: 16px;
    }
</style>'''
    conn = http.client.HTTPSConnection("beecloud.llschain.com")
    payload = json.dumps({
        "context": body,
        "name": "domain-notify",
        "type": "email",
        "subject": "域名测试通知",
    })
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjhlN2Y3NjU0LWUzZGEtNGY4OS1hZTZlLTdkN2RiMjY0NzA4YiJ9.eyJpc3MiOiJodHRwczovL2JlZWNsb3VkLmxsc2NoYWluLmNvbS91NS9hcGkvdjEiLCJzdWIiOiIxY2RjODllMi02NTNiLTRjOTEtYjM2YS05NmM3Y2U5ZWNlMWUiLCJleHAiOjE3MTc3NzQ3MzgsImlhdCI6MTcxNzcyNDMzOCwidGVuYW50X2lkIjoiOGI0MzRkOTctODdhYi00OWY5LWE4MmQtOGQzYzgyZGY2ZDVlIiwidGVuYW50X25hbWUiOiJsbHMiLCJ1c2VyX2lkIjoiMWNkYzg5ZTItNjUzYi00YzkxLWIzNmEtOTZjN2NlOWVjZTFlIiwidXNlcm5hbWUiOiJoYW5ib3dlbiJ9.HPNL4UecaGTO47ycYsvIPpJcN0z-qdsGSu4UtxtssjwzV_qidD-4-Pqko-eRQK0nbxwUBuSvb-m291OoSZpVZrDtQXy9MUiViPGgeoskYj-yrWzMTudrWgMjX7qHD7SfXsKaT2MOu30rz_gCfTWj-t_0ne6qIXZ3ZbkVCm97yt9e5Wx7T219aFORackXSw07oQwAcQLSVTxopCgsjOI0O6U59qyjfpz_rw2rxLdgO4QD6lBpPfOSXE9yp5AQedd-8eEsZRvBTIEmqKVM4DrX103iXyygLDSflzWbsVdD33JFRVZkeHrzOYnVPcDOCBc9pFHMAT4Wm_-qlccxtOxLNA',
        'Content-Type': 'application/json',
    }
    conn.request("POST", "/u5/api/v1/tenants/8b434d97-87ab-49f9-a82d-8d3c82df6d5e/notify/template", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


def apikey_template():
    body = '''<div>
        <includetail>
            <div style="font:Verdana normal 14px;color:#000;">
                <div style="position:relative;">
                    <div class="eml-w eml-w-sys-layout">
                        <div style="font-size: 0px;">
                            <div class="eml-w-sys-line">
                                <div class="eml-w-sys-line-left"></div>
                                <div class="eml-w-sys-line-right"></div>
                            </div>
                            <div class="eml-w-sys-logo" style="float: right">
                                <img src="data:image/png;base64,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" alt=""/>
                            </div>
                        </div>
                        <div class="eml-w-sys-content">
                            <div class="dragArea gen-group-list">
                                <div class="gen-item">
                                    <div class="eml-w-item-block" style="padding: 0px;">
                                        <div class="eml-w-title-level1">APIKEY通知</div>
                                    </div>
                                </div>
                                <div class="gen-item" draggable="false" style="margin-top: 16px;">
                                    <hr color="#E9E9E9" size="1"/>
                                    <div class="eml-w-item-block" style="padding: 0px 0px 0px 1px;">
                                        <div class="eml-w-title-level3">
                                            <span>您申请的APIKEY已经创建成功。信息如下：</span>
                                            <div style="margin-top: 16px;">
                                                <table style="font-size: 14px;">
                                                    <tr>
                                                        <td style="font-weight: 500">BaseURL：</td>
                                                        <td style="color: blue;">{{index . "base_url"}}</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="font-weight: 500">Model：</td>
                                                        <td style="color: blue;">{{index . "model"}}</td>
                                                    </tr>
                                                    <tr>
                                                        <td style="font-weight: 500">APIKEY：</td>
                                                        <td style="color: blue;">sk-{{index . "token"}}</td>
                                                    </tr>
                                                </table>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="eml-w-sys-footer">BeeCloud APIKEY</div>
                    </div>
                </div>
            </div><!--<![endif]-->
        </includetail>
    </div>

    <style>
        .eml-w-title-level1 {
            font-size: 20px;
            font-weight: 500;
            padding: 15px 0
        }

        .eml-w-title-level3 {
            font-size: 14px;
            font-weight: 500;
            padding-bottom: 10px
        }

        .eml-w-sys-layout {
            background: #fff;
            box-shadow: 0 2px 8px 0 rgba(0, 0, 0, .2);
            border-radius: 4px;
            margin: 50px auto;
            max-width: 800px;
            overflow: hidden
        }

        .eml-w-sys-line-left {
            display: inline-block;
            width: 88%;
            background: #0887FF;
            height: 3px
        }

        .eml-w-sys-line-right {
            display: inline-block;
            width: 11.5%;
            height: 3px;
            background: #0887FF;
            opacity: 0.7;
            margin-left: 1px
        }

        .eml-w-sys-logo {
            text-align: right
        }

        .eml-w-sys-logo img {
            display: inline-block;
            margin: 30px 50px 0 0
        }

        .eml-w-sys-content {
            position: relative;
            padding: 20px 50px 0;
            min-height: 216px;
            word-break: break-all
        }

        .eml-w-sys-footer {
            font-weight: 500;
            font-size: 12px;
            color: #bebebe;
            letter-spacing: .5px;
            padding: 0 0 30px 50px;
            margin-top: 60px
        }

        .eml-w {
            font-family: Helvetica Neue, Arial, PingFang SC, Hiragino Sans GB, STHeiti, Microsoft YaHei, sans-serif;
            -webkit-font-smoothing: antialiased;
            color: #2b2b2b;
            font-size: 14px;
            line-height: 1.75
        }

        .eml-w a {
            text-decoration: none
        }

        .eml-w a, .eml-w a:active {
            color: #186fd5
        }

        .eml-w h1, .eml-w h2, .eml-w h3, .eml-w h4, .eml-w h5, .eml-w h6, .eml-w li, .eml-w p, .eml-w ul {
            margin: 0;
            padding: 0
        }

        .eml-w-item-block {
            margin-bottom: 10px
        }

        @media (max-width: 420px) {
            .eml-w-sys-layout {
                border-radius: none !important;
                box-shadow: none !important;
                margin: 0 !important
            }

            .eml-w-sys-layout .eml-w-sys-line {
                display: none
            }

            .eml-w-sys-layout .eml-w-sys-logo img {
                margin-right: 30px !important
            }

            .eml-w-sys-layout .eml-w-sys-content {
                padding: 0 35px !important
            }

            .eml-w-sys-layout .eml-w-sys-footer {
                padding-left: 30px !important
            }
        }
        table tr td:first-child {
            width: 100px
        }
        table {
            font-size: 16px;
        }
    </style>'''
    conn = http.client.HTTPSConnection("beecloud.llschain.com")
    payload = json.dumps({
        "context": body,
        "name": "apikey-notify",
        "type": "email",
        "subject": "APIKEY创建成功通知",
    })
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjhlN2Y3NjU0LWUzZGEtNGY4OS1hZTZlLTdkN2RiMjY0NzA4YiJ9.eyJpc3MiOiJodHRwczovL2JlZWNsb3VkLmxsc2NoYWluLmNvbS91NS9hcGkvdjEiLCJzdWIiOiIxY2RjODllMi02NTNiLTRjOTEtYjM2YS05NmM3Y2U5ZWNlMWUiLCJleHAiOjE3MTc2OTYwNTgsImlhdCI6MTcxNzY0NTY1OCwidGVuYW50X2lkIjoiOGI0MzRkOTctODdhYi00OWY5LWE4MmQtOGQzYzgyZGY2ZDVlIiwidGVuYW50X25hbWUiOiJsbHMiLCJ1c2VyX2lkIjoiMWNkYzg5ZTItNjUzYi00YzkxLWIzNmEtOTZjN2NlOWVjZTFlIiwidXNlcm5hbWUiOiJoYW5ib3dlbiJ9.OSxMe483yQRe8vCKrC4dw2QJKWEbp4kgQCgkaNEapW8m5Dig7byKOdl5I0EizTA2QoZrDhBa46XDFJlqCtwcor9dFvK9H3EFPIR_D0wQGmYde2vkR3GHQCIC3_UZWZ1g18K5AzPyVFAeAyMZ1y8y68412WZQbQ7qU1MixbGqkxLN4P16vUtVwXogJ99veUrH7gfoHMhFI9nc6wJ5q-LOp79P6N245oWZjjsdnHmSqNkGvaKCufU0lwGjfEgx6Rf23TjEfwqlEjB0PnmCpxvyKthhW6tVGu-gjUQNTUTwO-BlKRnKaUgLWPxNj9KyVxNYDHXf-5ynvwoR_gQTVbAJmQ',
        'Content-Type': 'application/json',
    }
    conn.request("POST", "/u5/api/v1/tenants/8b434d97-87ab-49f9-a82d-8d3c82df6d5e/notify/template", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


domain_test_template()
