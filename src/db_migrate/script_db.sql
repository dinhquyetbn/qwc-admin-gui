CREATE TABLE qwc_config.pbms_quan_ly_nhom_tham_so (
	id VARCHAR(50) NOT NULL,
    ten_nhom VARCHAR(256) NOT NULL,
    thu_tu_hien_thi INTEGER DEFAULT 0 NOT NULL,
    nguoi_tao VARCHAR(50),
    ngay_tao TIMESTAMPTZ NOT NULL,
    nguoi_sua VARCHAR(50),
    ngay_sua TIMESTAMPTZ,
    nguoi_xoa VARCHAR(50),
    ngay_xoa TIMESTAMPTZ,
    trang_thai_xoa BOOLEAN DEFAULT false,
	CONSTRAINT pbms_quan_ly_nhom_tham_so_pk PRIMARY KEY (id)
);

GRANT REFERENCES, INSERT, UPDATE, TRUNCATE, TRIGGER, SELECT, DELETE ON TABLE qwc_config.pbms_quan_ly_nhom_tham_so TO qwc_admin;


CREATE TABLE qwc_config.pbms_quan_ly_tham_so (
	id VARCHAR(50) NOT NULL,
    ma_truong VARCHAR(50) NOT NULL,
    ten_truong VARCHAR(100) NOT NULL,
    kieu_du_lieu VARCHAR(256) NOT NULL,
    mo_ta VARCHAR(50) NOT NULL,
    thu_tu_hien_thi INTEGER DEFAULT 0 NOT NULL,
    nhom_tham_so_id VARCHAR(50) NOT NULL,
    nguoi_tao VARCHAR(50),
    ngay_tao TIMESTAMPTZ NOT NULL,
    nguoi_sua VARCHAR(50),
    ngay_sua TIMESTAMPTZ,
    nguoi_xoa VARCHAR(50),
    ngay_xoa TIMESTAMPTZ,
    trang_thai_xoa BOOLEAN DEFAULT false,
	CONSTRAINT pbms_quan_ly_tham_so_pk PRIMARY KEY (id)
);

GRANT REFERENCES, INSERT, UPDATE, TRUNCATE, TRIGGER, SELECT, DELETE ON TABLE qwc_config.pbms_quan_ly_tham_so TO qwc_admin;