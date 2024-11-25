var PBMSLang = {
    "zeroRecords": "Không có dữ liệu.",
    "emptyTable": "Không có dữ liệu.",
    "processing": "",
    "infoFiltered": "",
    "aria": {
        "sortAscending": ": Sắp xếp thứ tự tăng dần",
        "sortDescending": ": Sắp xếp thứ tự giảm dần"
    },
    "autoFill": {
        "cancel": "Hủy",
        "fill": "Điền tất cả ô với <i>%d<\/i>",
        "fillHorizontal": "Điền theo hàng ngang",
        "fillVertical": "Điền theo hàng dọc",
        "info": "Mẫu thông tin tự động điền"
    },
    "buttons": {
        "collection": "Chọn lọc <span class=\"ui-button-icon-primary ui-icon ui-icon-triangle-1-s\"><\/span>",
        "colvis": "Hiển thị theo cột",
        "colvisRestore": "Khôi phục hiển thị",
        "copy": "Sao chép",
        "copyKeys": "Nhấn Ctrl hoặc u2318 + C để sao chép bảng dữ liệu vào clipboard.<br \/><br \/>Để hủy, click vào thông báo này hoặc nhấn ESC",
        "copySuccess": {
            "1": "Đã sao chép 1 dòng dữ liệu vào clipboard",
            "_": "Đã sao chép %d dòng vào clipboard"
        },
        "copyTitle": "Sao chép vào clipboard",
        "csv": "File CSV",
        "excel": "File Excel",
        "pageLength": {
            "-1": "Xem tất cả các dòng",
            "1": "Hiển thị 1 dòng",
            "_": "Hiển thị %d dòng"
        },
        "pdf": "File PDF",
        "print": "In ấn"
    },
    "infoPostFix": "",
    "infoThousands": "`",
    "select": {
        "1": "%d dòng đang được chọn",
        "_": "%d dòng đang được chọn",
        "cells": {
            "1": "1 ô đang được chọn",
            "_": "%d ô đang được chọn"
        },
        "columns": {
            "1": "1 cột đang được chọn",
            "_": "%d cột đang được được chọn"
        },
        "rows": {
            "1": "1 dòng đang được chọn",
            "_": "%d dòng đang được chọn"
        }
    },
    "thousands": "`",
    "searchBuilder": {
        "title": {
            "_": "Tìm kiếm mở rộng (%d)",
            "0": "Tìm kiếm mở rộng"
        },
        "button": {
            "0": "Tìm kiếm mở rộng",
            "_": "Tìm kiếm mở rộng (%d)"
        },
        "value": "Giá trị",
        "clearAll": "Xóa hết",
        "condition": "Điều kiện",
        "conditions": {
            "date": {
                "after": "Sau",
                "before": "Trước",
                "between": "Nằm giữa",
                "empty": "Rỗng",
                "equals": "Bằng với",
                "not": "Không phải",
                "notBetween": "Không nằm giữa",
                "notEmpty": "Không rỗng"
            },
            "number": {
                "between": "Nằm giữa",
                "empty": "Rỗng",
                "equals": "Bằng với",
                "gt": "Lớn hơn",
                "gte": "Lớn hơn hoặc bằng",
                "lt": "Nhỏ hơn",
                "lte": "Nhỏ hơn hoặc bằng",
                "not": "Không phải",
                "notBetween": "Không nằm giữa",
                "notEmpty": "Không rỗng"
            },
            "string": {
                "contains": "Chứa",
                "empty": "Rỗng",
                "endsWith": "Kết thúc bằng",
                "equals": "Bằng",
                "not": "Không phải",
                "notEmpty": "Không rỗng",
                "startsWith": "Bắt đầu với"
            }
        },
        "logicAnd": "Và",
        "logicOr": "Hoặc",
        "add": "Thêm điều kiện",
        "data": "Dữ liệu",
        "deleteTitle": "Xóa quy tắc lọc"
    },
    "searchPanes": {
        "countFiltered": "{shown} ({total})",
        "emptyPanes": "Không có phần tìm kiếm",
        "clearMessage": "Xóa hết",
        "loadMessage": "Đang load phần tìm kiếm",
        "collapse": {
            "0": "Phần tìm kiếm",
            "_": "Phần tìm kiếm (%d)"
        },
        "title": "Bộ lọc đang hoạt động - %d",
        "count": "{total}"
    },
    "datetime": {
        "hours": "Giờ",
        "minutes": "Phút",
        "next": "Sau",
        "previous": "Trước",
        "seconds": "Giây"
    },
    "info": "Hiển thị _START_ tới _END_ của _TOTAL_ bản ghi",
    "infoEmpty": "Tổng 0 bản ghi",
    "lengthMenu": "_MENU_",
    "loadingRecords": "Đang tải...",
    "paginate": {
        "first": "Đầu tiên",
        "last": "Cuối cùng",
        "next": ">",
        "previous": "<"
    },
    "search": "Tìm kiếm:",
    "editor": {
        "close": "Đóng",
        "create": {
            "button": "Thêm mới",
            "title": "Tạo dữ liệu mới",
            "submit": "Lưu thay đổi"
        },
        "edit": {
            "button": "Chỉnh sửa",
            "title": "Chỉnh sửa dữ liệu",
            "submit": "Lưu thay đổi"
        },
        "remove": {
            "button": "Xóa",
            "title": "Xóa",
            "submit": "Xóa",
            "confirm": {
                "_": "Are you sure you wish to delete %d rows?",
                "1": "Are you sure you wish to delete 1 row?"
            }
        }
    }    
}

function getIdxFieldTable(arrs, vals) {
    let result = [];
    vals.forEach(element => {
        result.push(arrs.indexOf(element));
    });
    return result;
}