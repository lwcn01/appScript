/**
 * 
 * @authors Your Name (you@example.org)
 * @date    2016-01-26 16:03:36
 * @version $Id$
 */
#把JavaScript代码放到<head>中,<script>...</script>包含的代码就是JavaScript代码,将直接被浏览器执行
<html>
<head>
  <script>
    alert('Hello, world');
  </script>
</head>
<body>
  ...
</body>
</html>

#把JavaScript代码放到一个单独的.js文件，然后在HTML中通过<script src="..."></script>引入这个文件
<html>
<head>
  <script src="/static/js/abc.js"></script>
</head>
<body>
  ...
</body>
</html>

#console.log('xxx'); 浏览器开发者调试模式

