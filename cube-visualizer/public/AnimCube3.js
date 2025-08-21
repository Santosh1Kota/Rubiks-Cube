/* AnimCube3 loader shim: fetch official script from CDN if local not bundled */
(function(){
  if (typeof window === "undefined" || window.AnimCube3) return;
  var s = document.createElement("script");
  s.src = "https://cdn.jsdelivr.net/gh/cubing/AnimCubeJS/AnimCube3.js";
  s.async = true;
  (document.currentScript && document.currentScript.parentNode
    ? document.currentScript.parentNode
    : document.body).appendChild(s);
})();


