var mainPlatform = {

	init: function(){

		this.bindEvent();
		// this.render(menu['home']);
	},

	bindEvent: function(){
		var self = this;
		// 顶部大菜单单击事件
		$(document).on('click', '.pf-nav-item', function() {
            $('.pf-nav-item').removeClass('current');
            $(this).addClass('current');

            // 渲染对应侧边菜单
            var m = $(this).data('menu');
            self.render(menu[m]);
        });

        $(document).on('click', '.sider-nav li', function() {
            $('.sider-nav li').removeClass('current');
            $(this).addClass('current');
            $('iframe').attr('src', $(this).data('src'));
        });

        $(document).on('click', '.pf-logout', function() {
            layer.confirm('您确定要退出吗？', {
              icon: 4,
			  title: '确定退出' //按钮
			}, function(){
			  location.href= 'login.html'; 
			});
        });
        //左侧菜单收起
        $(document).on('click', '.toggle-icon', function() {
            $(this).closest("#pf-bd").toggleClass("toggle");
            setTimeout(function(){
            	$(window).resize();
            },300)
        });

        $(document).on('click', '.pf-modify-pwd', function() {
            $('#pf-page').find('iframe').eq(0).attr('src', 'backend/modify_pwd.html')
        });

        $(document).on('click', '.pf-notice-item', function() {
            $('#pf-page').find('iframe').eq(0).attr('src', 'backend/notice.html')
        });
	},
	render: function(menu){
		
		if(menu == null)
		{
			alert("请先定义菜单！，格式请参考menu.js");
			return;
		}
		
		var current,html='',menuLi='';
/*			
左侧菜单的HTML结构。
                  <li class="current">
                        <a href="javascript:;">
                            <span class="iconfont sider-nav-icon">&#xe620;</span>
                            <span class="sider-nav-title">供应商组织</span>
                            <i class="iconfont">&#xe642;</i>
                        </a>
                        <ul class="sider-nav-s">
                           <li class="active"><a href="javascript:void(0);" onClick="openTab('.easyui-tabs1','供应商组织1','http://www.baidu.com')">供应商组织1</a></li>
                           <li class=""><a href="javascript:void(0);" onClick="openTab('.easyui-tabs1','表单管理','providers1.html')">表单管理</a></li>
                           <li><a href="#">供应商组织2</a></li>
                           <li><a href="#">供应商组织3</a></li>
                           <li><a href="#">供应商组织4</a></li>
                        </ul>
                     </li>*/
		for(var i = 0, len = menu.menu.length; i < len; i++){
			    //alert("二级菜单="+menu.menu[i].icon);
				//console.log(menu.menu[i].menu);
				var current = (i == 0) ? ' class="current"' : '';
				var menuLi = '';
				html = html + '<li'+current+'><a href="javascript:;"><span class="iconfont sider-nav-icon">'+menu.menu[i].icon+'</span><span class="sider-nav-title">'+menu.menu[i].title+'</span><i class="iconfont">&#xe642;</i></a><ul class="sider-nav-s">';
						for(var m = 0, len2 = menu.menu[i].menu.length; m < len2; m++)
						{
							//alert("获取三级菜单");
							//alert("二级菜单="+menu.menu[i].title+"下的三级菜单="+menu.menu[i].menu[m].title);
							var active = (m == 0) ? ' class="active"' : '';
							menuLi = menuLi + '<li '+active+'><a href="javascript:void(0);" onClick="openTab(\'.easyui-tabs1\',\''+menu.menu[i].menu[m].title+'\',\''+menu.menu[i].menu[m].href+'\')">'+menu.menu[i].menu[m].title+'</a></li>';
						}
						html = html+menuLi+'</ul></li>';
		}
		$('#pf-sider').find(".sider-nav").html(html);
	}

};

mainPlatform.init();