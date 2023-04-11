// nav 높이 + container 높이 + footer 높이 < viewport 높이
// : footer 요소를 viewport 아래에 fixed
// nav 높이 + container 높이 + footer 높이 >= viewport 높이
// : footer 요소에 fixed 제거

let nav_h = document.querySelector(".navbar").clientHeight;
let con_h = document.querySelector("div.contents").clientHeight;
let footer_h = document.querySelector("footer").clientHeight;

console.log(nav_h, con_h, footer_h)
console.log(window.innerHeight)
doc_h = nav_h + con_h + footer_h
if (doc_h >= window.innerHeight){
  document.querySelector('footer').classList.remove('fixed-bottom')
}