$(function () {
    // =========================== 全局变量 ===================================== \\
    /* 项目根路径 */
    var strFullPath = window.document.location.href;
    var strPath = window.document.location.pathname;
    var pos = strFullPath.indexOf(strPath);
    var basePath = strFullPath.substring(0, pos);

    // =========================== 初始化 ===================================== \\
    $('#dg').datagrid({
        url: basePath + '/base/all',
        // data: [{'id':'1', 'linked_co__name': '测试'}],
        columns: [[
            {field: 'ck', title: 'ck', checkbox: true},
            {field: 'id', title: '序号', hidden: true},
            {field: 'pro_name', title: '项目名称', align: 'center'},
            {field: 'linked_co__text', title: '挂靠公司'},
            {field: 'district__text', title: '区域'},
            {field: 'internal_no', title: '内部文号'},
            {field: 'pro_type__text', title: '项目类型'},
            {field: 'pro_no', title: '项目编号'},
            {field: 'task_code', title: '任务编号'},
            {field: 'predict', title: '预计信息点'},
        ]],
        pagination: true,
        toolbar: '#tb',
        pageSize: 10,
        striped: true,
        rownumbers: true,
        fitColumns: true,
        checkbox: true
    });

    /* 初始化编辑对话框 */
    $('#dialog').dialog({
        title: '录入工程基本信息',
        width: 400,
        height: 200,
        closed: true,
        cache: false,
        href: 'get_content.php',
        modal: true
    });

    /* 下拉框初始化 */
    $('#c_linked_co').combobox({
        url: basePath + '/base/linked_co',
        valueField: 'id',
        textField: 'text'
    });

    $('#c_district').combobox({
        url: basePath + '/base/district',
        valueField: 'id',
        textField: 'text'
    });

    $('#c_pro_type').combobox({
        url: basePath + '/base/pro_type',
        valueField: 'id',
        textField: 'text'
    });

    // =========================== 事件绑定 ===================================== \\
    $('#add').click(function () {
        $('#dlg').dialog('open').dialog('setTitle', '录入');
        // 设置表单新增模式url
        $('#fm').form('clear');
        $('#fm').form({
            url: basePath + '/base/add',
            success: function (data) {
                $('#dg').datagrid('reload');
                if (data) {
                    data = JSON.parse(data);
                    alert(data.mess);
                }
            }
        });
    });

    $('#edit').click(function () {
        var targets = $('#dg').datagrid('getChecked');
        var id = targets[0].id; // 选中多行的时候编辑第一个
        // 编辑时候先将编辑对象的信息加载到表单
        $('#fm').form('load', basePath + '/base/get_by_id/' + id);
        $('#dlg').dialog('open');
        // 设置表单编辑模式url
        $('#fm').form({
            url: basePath + '/base/edit/' + id,
            success: function (data) {
                $('#dg').datagrid('reload');
                // if (data) {
                //     alert(data.mess);
                // }
            }
        });
    });

    $('#delete').click(function () {
        var targets = $('#dg').datagrid('getChecked');
        var ids = [];
        $.each(targets, function (index, item) {
            ids.push(item.id);
        });
        $.ajax({
            type: "GET",
            url: basePath + '/base/fake_delete',
            // cache : false,
            // traditional: true,
            contentType: 'application/json',
            dataType: 'json',
            data: {'ids[]': ids},
            success: function (data) {
                if (data) {
                    alert(data.mess);
                    $('#dg').datagrid('reload');
                }
            }
        });
    });

    // 单机保存时候提交表单
    $('#save').click(function () {
        $('#fm').submit();
        $('#dlg').dialog('close');
        // $('#dg').datagrid('reload');
    });

    // =========================== 函数 ===================================== \\

});
