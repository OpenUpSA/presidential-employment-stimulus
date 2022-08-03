function transformDOM(window) {
  const tag = window.document.createElement('script');
  tag.setAttribute('src', 'js/index.js');
  window.document.body.appendChild(tag);

  addScriptToBody(window, {src:'https://www.googletagmanager.com/gtag/js?id=G-45HV67WN3P'},''); 

  addScriptToBody(window, {}, 'window.dataLayer = window.dataLayer || [];\
    function gtag(){dataLayer.push(arguments);}\
    gtag("js", new Date());\
    gtag("config", "G-45HV67WN3P");');
}
  

function addScriptToBody(window, attrs, text) {
  // Adding a script tag to body via jQuery seems to add it to head as well
  const tag = window.document.createElement("script");
  for (let name in attrs)
    tag.setAttribute(name, attrs[name]);
  if (text)
    tag.appendChild(window.document.createTextNode(text));

  window.document.body.appendChild(tag);
  window.document.body.appendChild(window.document.createTextNode("\n"));
}

exports.transformDOM = transformDOM;
