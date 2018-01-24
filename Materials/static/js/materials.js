$(function () {
    // =========================== 全局变量 ===================================== \\
    /* 项目根路径 */
    var strFullPath = window.document.location.href;
    var strPath = window.document.location.pathname;
    var pos = strFullPath.indexOf(strPath);
    var basePath = strFullPath.substring(0, pos);

    // =========================== 初始化 ===================================== \\
    $('#dg').datagrid({
        url: basePath + '/material/list',
        columns: [[
            {field: 'ck', title: 'ck', checkbox: true},
            {field: 'material_situation', title: '主键', hidden: true},
            {field: 'project__pro_name', title: '项目名称', align: 'center'},
            {field: 'expected_scale', title: '设计量'},
            {field: 'lis_scale', title: 'LIS量'},
            {field: 'good_arrived_scale', title: '到货量'},
            {field: 'memo', title: '备注'}
        ]],
        pagination: true,
        toolbar: '#tb',
        pageSize: 10,
        striped: true,
        rownumbers: true,
        fitColumns: true,
        checkbox: true
    });

    /* 初始化信息编辑对话框 */
    $('#edit_dialog').dialog({
        title: '录入工程材料情况',
        width: 300,
        height: 300,
        closed: true,
        cache: false,
        modal: true,
        buttons: '#dlg-buttons'
    });

    /* 初始化Excel上传对话框 */
    $('#upload_dialog').dialog({
        title: '导入Excel文件',
        width: 300,
        height: 200,
        closed: true,
        cache: false,
        modal: true,
        buttons: '#excel-buttons'
    });

    $('#fb').filebox({
        buttonText: '选择文件',
        buttonAlign: 'left'
    });

    /**
     * 初始化项目选择器
     *
     * 初始化时加载最新前10项目
     * 当输入为空的时候加载最新前10的项目
     * */
    $('#cc').combobox({
        url: basePath + '/base/get_top_10_pro',
        valueField: 'id',
        textField: 'pro_name',
        mode: 'remote'
    });


    // /* 下拉框初始化 */
    // $('#c_linked_co').combobox({
    //     url: basePath + '/base/linked_co',
    //     valueField: 'id',
    //     textField: 'text'
    // });
    //
    // $('#c_district').combobox({
    //     url: basePath + '/base/district',
    //     valueField: 'id',
    //     textField: 'text'
    // });
    //
    // $('#c_pro_type').combobox({
    //     url: basePath + '/base/pro_type',
    //     valueField: 'id',
    //     textField: 'text'
    // });

    // =========================== 事件绑定 ===================================== \\
    $('#add').click(function () {
        $('#edit_dialog').dialog('open').dialog('setTitle', '录入');
        // 设置表单新增模式url
        $('#fm').form('clear');
        $('#fm').form({
            url: basePath + '/material/add',
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
        var id = targets[0].material_situation; // 选中多行的时候编辑第一个
        // 编辑时候先将编辑对象的信息加载到表单
        $('#fm').form('load', basePath + '/material/get_by_id/' + id);
        $('#edit_dialog').dialog('open');
        // 设置表单编辑模式url
        $('#fm').form({
            url: basePath + '/material/edit/' + id,
            success: function (data) {
                $('#dg').datagrid('reload');
                if (data) {
                    data = JSON.parse(data);
                    alert(data.mess);
                }
            }
        });
    });

    $('#delete').click(function () {
        var targets = $('#dg').datagrid('getChecked');
        var ids = [];
        $.each(targets, function (index, item) {
            ids.push(item.material_situation);
        });
        $.ajax({
            type: "GET",
            url: basePath + '/material/fake_delete',
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

    // 单击保存时候提交表单
    $('#save').click(function () {
        if ($('#fm').form('validate')) {
            $('#fm').submit();
            $('#edit_dialog').dialog('close');
        } else {
            alert('信息有误！');
        }

        // $('#dg').datagrid('reload');
    });

    $('#import').click(function () {
        $('#upload_dialog').dialog('open');
    })

    $('#excel_save').click(function () {
        $('#excel_form').form({
            url: basePath + '/base/import_excel',
            // data: $("#excel_form").serialize(),
            success: function (data) {
                if (data) {
                    data = JSON.parse(data);
                    alert(data.mess);
                }
            }
        });
        $('#excel_form').form('submit');
    })

    // =========================== 工具函数 ===================================== \\
    function search_pro() {
        var value = $('#cc').combobox('getText');
        console.log(value);
        var s;
        s['keyword'] = value;
        if (value) {
            $.ajax({
                type: "POST",
                url: basePath + '/material/search_pro',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(s),
                success: function (data) {
                    if (data.result) {
                        // $('#cc').combobox('setValue', data.result);

                    }

                    if (data.mess) {
                        alert(data.mess);
                    }
                }
            });
        }

    }
});
