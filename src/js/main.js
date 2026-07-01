// myself_web - 主站 JavaScript
console.log('🧑 myself_web 已加载');

// 页面滚动导航栏效果
document.addEventListener('DOMContentLoaded', () => {
  const navbar = document.querySelector('.navbar');
  
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.style.borderBottom = '1px solid rgba(56, 189, 248, 0.2)';
    } else {
      navbar.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
    }
  });
});
