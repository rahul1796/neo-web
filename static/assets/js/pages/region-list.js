var varTable;
$(document).ready(function () {
    $("#tbl_region").dataTable().fnDestroy();
    LoadTable(); 
    role_id=parseInt($('#hdn_home_user_role_id').val());
    if(role_id == 5)
        $('#btn_create').hide();
});

function LoadTable()
{
    vartable1 = $("#tbl_region").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/region_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.region_id = 0;
            },
            error: function (e) {
                $("#tbl_region tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {"visible": false,
            "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(role_id != 5)
                        varButtons += '<a onclick="EditRegionDetail(\'' + row.Region_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Client" class="fas fa-edit" ></i></a>';
                    return varButtons;
                }
            },
            { "data": "Region_Name" },
            { "data": "Region_Code" },
            { "data": function (row, type, val, meta) {
                var varStatus = ""; 
                if(row.Is_Active)
                    varStatus="Active";
                else
                    varStatus="In Active";
                return varStatus;
                }
            }
        ],
        drawCallback: function(){
            $('#tbl_region_paginate ul.pagination').addClass("pagination-rounded");
        }

    });
}
function EditRegionDetail(RegionId)
{
    $('#hdn_region_id').val(RegionId);
    $('#form1').submit();
    
}