> 因为工作需要Ajax轮询，所以用Flask实现了 Ajax异步加载、Ajax轮询。分别写个简单的小例子简要总结一下

### Ajax
AJAX = Asynchronous JavaScript and XML（异步的 JavaScript 和 XML）。
AJAX 是在不重新加载整个页面的情况下,与服务器交换数据并更新部分网页的艺术。

### 异步加载

直接上代码

**Flask部分：**

	from flask import Flask, jsonify, render_template, request

	app = Flask(__name__)

	@app.route('/add')
	def add():
		num = request.args.get('num', 0, type=int)
		data = num + 1
		return jsonify(data)

	@app.route('/')
	def index():
		return render_template('index.html')

	if __name__ == '__main__':
		app.run()

add函数中request.args.get('num', 0, type=int)如果参数num不存在，一个默认值(这里是 0)将被返回。更进一步，我们还可以将值转换为一个特定类型(就像我们这里的 int 类型)

**HTML部分：**

	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.js"></script>
	<script>window.jQuery || document.write('<script src="{{ url_for('static', filename='jquery.js') }}">\x3C/script>')</script>

	<script type=text/javascript>
	  $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
	 $(function() {
		$('a#add').bind('click', function() {
		  $.getJSON($SCRIPT_ROOT + '/add', {
			num: $('#result').text()
		  }, function(data) {
			$("#result").text(data);
		  });
		  return false;
		});
	  });

	</script>

	<span id=result>1</span>
	<a href=# id=add>add</a>

如果在自备梯子的情况下以上代码就可以直接运行了，否则的话自行下载jQuery，并导入

**SCRIPT_ROOTL**:一个全局变量作为一个应用根路径的前缀
js代码解释：
监听id为add的超链接，当其被点击时发送请求，请求url为/add,参数num的值是id=reault的text部分的值（此处是1）
Flask程序执行完返回num+1（此时是2），然后再将这个返回值替换掉id为result的text部分的值（是不是很详细..）

**以上程序运行效果为：点一次add链接，值就加1， 点一次add链接，值就加1**

### Ajax轮询

Flask部分代码不变
JS部分改变：

	<script type=text/javascript>
	  $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
	  function GetState() {
		  $.getJSON($SCRIPT_ROOT + '/add', {
				num: $('#result').text()
			  }, function(data) {
			$("#result").text(data);
		  });
		};

	$(function() {
	  $('a#add').bind('click', function(){
			  setInterval("GetState()", 1000);
	  })
	  });
	</script>

setInterval() 方法可按照指定的周期（以毫秒计）来调用函数或计算表达式。
所以和上一个改变在每隔一秒发送一个请求

**以上程序运行效果为：点一次add链接，值就一直就加1**


![](http://oumkbl9du.bkt.clouddn.com/2017-09-08-2GG8A-ajax.png)

