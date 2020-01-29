var varTable;
$(document).ready(function () {
    $("#tbl_users").dataTable().fnDestroy();
    LoadTable(); 
    role_id=parseInt($('#hdn_home_user_role_id').val());
    // if(role_id == 5 || role_id == 1)
    //     $('#btn_create').show();
});

function LoadTable()
{
    vartable1 = $("#tbl_users").DataTable({
        "serverSide": true,
        "aLengthMenu": [[10, 25, 50], [10, 25, 50]],
        "paging": true,
        "pageLength": 10,
        "sPaginationType": "full_numbers",
        "scrollX": false,
        "destroy": true,
        "processing": true,
        "language": { "processing": 'Loading..!' },
        "ajax": {
            "url": $('#hdn_web_url').val()+ "/trainer_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.user_id = $('#hdn_home_user_id').val();
				d.user_role_id = $('#hdn_home_user_role_id').val();
            },
            error: function (e) {
                $("#tbl_users tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {"visible": false,
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                if(role_id == 5 || role_id==1 || role_id==15)
                    varButtons += '<a onclick="EditUserDetail(\'' + row.User_Id + '\',\'' + row.User_Role_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit User" class="fas fa-edit" ></i></a>';
                return varButtons;
                }
            },
            { "data": "User_Name" },
            { "data": "Email" },
            
			{ "data": function (row, type, val, meta) {
                var varStatus = ""; 
                if(row.Is_Active)
                    varStatus="Active";
                else
                    varStatus="In Active";
                return varStatus;
                }
            },
			{ "visible":false, "data": "Center_Name" },
            { "data": "Mobile_Number"}
           
            
        ],
        drawCallback: function(){
            $('#tbl_users_paginate ul.pagination').addClass("pagination-rounded");
        }

    });
}
function EditUserDetail(UserId,UserRoleId)
{
    $('#hdn_user_id').val(UserId);
    //alert('Hi');
    $('#form1').submit();
    
}
