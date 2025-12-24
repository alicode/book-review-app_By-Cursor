// 主要 JavaScript 檔案
document.addEventListener('DOMContentLoaded', function() {
    // Flash 訊息自動關閉（可選）
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(function(flash) {
        setTimeout(function() {
            flash.style.opacity = '0';
            flash.style.transition = 'opacity 0.5s';
            setTimeout(function() {
                flash.remove();
            }, 500);
        }, 5000);
    });
});



