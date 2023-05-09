// ==UserScript==
// @name         ChatMark
// @namespace    http://mallocx.com/
// @version      0.1
// @description  标记ChatGPT元素，提高RPA成功率
// @author       YanYang
// @match        https://chat.openai.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=tampermonkey.net
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // 创建复制按钮元素
    function createCopyButton(){
        var button = document.createElement('button');

        // 设置按钮属性和样式
        button.setAttribute('id', 'catcopy');
        button.textContent = 'copy';
        button.style.position = 'fixed';
        button.style.right = '0px';
        button.style.top = '0px';
        button.style.width = '30px';
        button.style.height = '20px';
        button.style.fontSize = '10px';
        button.style.backgroundColor = '#FF0000';
        button.style.color = '#FFFFFF';

        // 添加按钮到DOM树中
        const targetElement = document.querySelector('body');
        targetElement.appendChild(button);

        // 为按钮添加事件
        targetElement.addEventListener('click', function(event) {
            if (event.target === button) {

                const copybutton = document.querySelectorAll('[class*=flex][class*="ml-auto"][class*="gap-2"][class*="rounded-md"][class*="p-1"]');
                if (copybutton.length > 0){
                    copybutton[copybutton.length-1].click()
                    console.log('复制最后一个问题答案');
                }
                else{
                    console.log('没有找到复制按钮');
                };
            };
        });
    };

    // 标记文本框位置
    function modifyTextareas(){
        const textareas = document.querySelectorAll('[class*="m-"][class*="w-full"][class*="resize-none"][class*="border-0"][class*="bg-transparent"][class*="pl-"][class*="pr-"][class*="focus:ring-0"][class*="focus-visible:ring-0"][class*="dark:bg-transparent"][class*="md:pl-"]');
        if (textareas.length > 0) {
            textareas[0].style.backgroundColor = 'yellow';
        };
    };

    // 页面加载完成后开始工作
    window.onload = function() {
        console.log('Hello ChatMark');
        // 创建复制按钮
        createCopyButton();

        // 标记文本框位置
        modifyTextareas();

        // 监听body节点
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                const copybutton = document.querySelectorAll('[class*=flex][class*="ml-auto"][class*="gap-2"][class*="rounded-md"][class*="p-1"]');
                const respbutton = document.querySelector('[class*=btn][class*="relative"][class*="btn-neutral"][class*="border"][class*="md"]');
                const childElements = respbutton.children;
                for (let i = 0; i < childElements.length; i++) {
                    // 正在生成答案
                    if (childElements[i].textContent.includes('Stop')){
                        const catcopyButton = document.getElementById('catcopy')
                        catcopyButton.style.backgroundColor = '#D0D0D0';
                        console.log("正在生成答案" );
                    };
                    // 答案已完成
                    if (childElements[i].textContent.includes('Regenerat')){
                        const catcopyButton = document.getElementById('catcopy')
                        catcopyButton.style.backgroundColor = '#FF0000';
                        console.log("答案已生成" );
                    };
                };
                // 页面刷新后，重新标记文本框位置
                modifyTextareas();
            });
        });

        // 监听开始
        observer.observe(document.body, {
            childList:true,
            subtree: true,
        });

        // 监听发送按钮事件
        const sendButton = document.querySelector('[class*="absolute"][class*="rounded-md"][class*="bottom-"][class*="right-"][class*="disabled"]');
        sendButton.addEventListener('click', function() {
            console.log("发送按钮被点击" );
            document.getElementById('catcopy').style.backgroundColor = '#D0D0D0';
        });
    };
})();