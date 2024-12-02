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

CREATE TABLE qwc_config.pbms_quan_ly_phan_loai_tai_san (
	id VARCHAR(50) NOT NULL,
    ten_loai_ts VARCHAR(256) NOT NULL,
    ds_tham_so TEXT,
    mo_ta VARCHAR(50) NOT NULL,
    nguoi_tao VARCHAR(50),
    ngay_tao TIMESTAMPTZ NOT NULL,
    nguoi_sua VARCHAR(50),
    ngay_sua TIMESTAMPTZ,
    nguoi_xoa VARCHAR(50),
    ngay_xoa TIMESTAMPTZ,
    trang_thai_xoa BOOLEAN DEFAULT false,
	CONSTRAINT pbms_quan_ly_phan_loai_tai_san_pk PRIMARY KEY (id)
);

GRANT REFERENCES, INSERT, UPDATE, TRUNCATE, TRIGGER, SELECT, DELETE ON TABLE qwc_config.pbms_quan_ly_phan_loai_tai_san TO qwc_admin;

CREATE TABLE qwc_config.pbms_dm_tinh_thanh (
	ma VARCHAR(5) NOT NULL,
    ten VARCHAR(256) NOT NULL,
    cap VARCHAR(100),
    nguoi_tao VARCHAR(50),
    ngay_tao TIMESTAMPTZ NOT NULL,
    nguoi_sua VARCHAR(50),
    ngay_sua TIMESTAMPTZ,
    nguoi_xoa VARCHAR(50),
    ngay_xoa TIMESTAMPTZ,
    trang_thai_xoa BOOLEAN DEFAULT false,
	CONSTRAINT pbms_dm_tinh_thanh_pk PRIMARY KEY (ma)
);

GRANT REFERENCES, INSERT, UPDATE, TRUNCATE, TRIGGER, SELECT, DELETE ON TABLE qwc_config.pbms_dm_tinh_thanh TO qwc_admin;

CREATE TABLE qwc_config.pbms_dm_quan_huyen (
	ma VARCHAR(5) NOT NULL,
    ten VARCHAR(256) NOT NULL,
    cap VARCHAR(100),
    ma_tp VARCHAR(5) NOT NULL,
    ten_tp VARCHAR(256) NOT NULL,
    nguoi_tao VARCHAR(50),
    ngay_tao TIMESTAMPTZ NOT NULL,
    nguoi_sua VARCHAR(50),
    ngay_sua TIMESTAMPTZ,
    nguoi_xoa VARCHAR(50),
    ngay_xoa TIMESTAMPTZ,
    trang_thai_xoa BOOLEAN DEFAULT false,
	CONSTRAINT pbms_dm_quan_huyen_pk PRIMARY KEY (ma)
);

GRANT REFERENCES, INSERT, UPDATE, TRUNCATE, TRIGGER, SELECT, DELETE ON TABLE qwc_config.pbms_dm_quan_huyen TO qwc_admin;

CREATE TABLE qwc_config.pbms_dm_phuong_xa (
	ma VARCHAR(5) NOT NULL,
    ten VARCHAR(256) NOT NULL,
    cap VARCHAR(100),
    ma_qh VARCHAR(5) NOT NULL,
    ten_qh VARCHAR(256) NOT NULL,
    ma_tp VARCHAR(5) NOT NULL,
    ten_tp VARCHAR(256) NOT NULL,
    nguoi_tao VARCHAR(50),
    ngay_tao TIMESTAMPTZ NOT NULL,
    nguoi_sua VARCHAR(50),
    ngay_sua TIMESTAMPTZ,
    nguoi_xoa VARCHAR(50),
    ngay_xoa TIMESTAMPTZ,
    trang_thai_xoa BOOLEAN DEFAULT false,
	CONSTRAINT pbms_dm_phuong_xa_pk PRIMARY KEY (ma)
);

GRANT REFERENCES, INSERT, UPDATE, TRUNCATE, TRIGGER, SELECT, DELETE ON TABLE qwc_config.pbms_dm_phuong_xa TO qwc_admin;

CREATE TABLE qwc_config.pbms_quan_ly_don_vi (
	id VARCHAR(50) NOT NULL,
    ma_dv VARCHAR(100) NOT NULL,
    ten_dv VARCHAR(500) NOT NULL,
    dia_chi VARCHAR(500),
    ma_px VARCHAR(5) NOT NULL,
    ten_px VARCHAR(256) NOT NULL,
    ma_qh VARCHAR(5) NOT NULL,
    ten_qh VARCHAR(256) NOT NULL,
    ma_tp VARCHAR(5) NOT NULL,
    ten_tp VARCHAR(256) NOT NULL,
    sdt VARCHAR(50),
    don_vi_cap_cha_id VARCHAR(50),
    nguoi_tao VARCHAR(50),
    ngay_tao TIMESTAMPTZ NOT NULL,
    nguoi_sua VARCHAR(50),
    ngay_sua TIMESTAMPTZ,
    nguoi_xoa VARCHAR(50),
    ngay_xoa TIMESTAMPTZ,
    trang_thai_xoa BOOLEAN DEFAULT false,
	CONSTRAINT pbms_quan_ly_don_vi_pk PRIMARY KEY (id)
);

GRANT REFERENCES, INSERT, UPDATE, TRUNCATE, TRIGGER, SELECT, DELETE ON TABLE qwc_config.pbms_quan_ly_don_vi TO qwc_admin;

CREATE TABLE qwc_config.pbms_quan_ly_dat_cong (
	id VARCHAR(50) NOT NULL,
    ma_dat VARCHAR(50) NOT NULL,
    ten_dat VARCHAR(256) NOT NULL,
    don_vi_quan_ly_id VARCHAR(50),
    hien_trang_sd_id VARCHAR(50),
    so_to INTEGER,
    so_thua INTEGER,
    dien_tich FLOAT,
    dia_chi VARCHAR(500),
    ma_px VARCHAR(5) NOT NULL,
    ten_px VARCHAR(256) NOT NULL,
    ma_qh VARCHAR(5) NOT NULL,
    ten_qh VARCHAR(256) NOT NULL,
    ma_tp VARCHAR(5) NOT NULL,
    ten_tp VARCHAR(256) NOT NULL,
    ds_file_dinh_kem TEXT,
    nguoi_tao VARCHAR(50),
    ngay_tao TIMESTAMPTZ NOT NULL,
    nguoi_sua VARCHAR(50),
    ngay_sua TIMESTAMPTZ,
    nguoi_xoa VARCHAR(50),
    ngay_xoa TIMESTAMPTZ,
    trang_thai_xoa BOOLEAN DEFAULT false,
	CONSTRAINT pbms_quan_ly_dat_cong_pk PRIMARY KEY (id)
);

GRANT REFERENCES, INSERT, UPDATE, TRUNCATE, TRIGGER, SELECT, DELETE ON TABLE qwc_config.pbms_quan_ly_dat_cong TO qwc_admin;

CREATE TABLE qwc_config.pbms_quan_ly_danh_muc (
    id VARCHAR(50) NOT NULL,
    ma_danh_muc VARCHAR(50) NOT NULL,
    ten_danh_muc VARCHAR(256) NOT NULL,
    ma_nhom VARCHAR(50) NOT NULL,
    ten_nhom VARCHAR(50) NOT NULL,
    nguoi_tao VARCHAR(50),
    ngay_tao TIMESTAMPTZ NOT NULL,
    nguoi_sua VARCHAR(50),
    ngay_sua TIMESTAMPTZ,
    nguoi_xoa VARCHAR(50),
    ngay_xoa TIMESTAMPTZ,
    trang_thai_xoa BOOLEAN DEFAULT false,
    CONSTRAINT pbms_quan_ly_danh_muc_pk PRIMARY KEY (id)
);

GRANT REFERENCES, INSERT, UPDATE, TRUNCATE, TRIGGER, SELECT, DELETE ON TABLE qwc_config.pbms_quan_ly_danh_muc TO qwc_admin;

CREATE TABLE qwc_config.pbms_quan_ly_nha_cong_san (
	id VARCHAR(50) NOT NULL,
    he_thong_id VARCHAR(50) NOT NULL,
    tai_san_id VARCHAR(50) NOT NULL,
    tai_san_theo_chu_so_huu_id VARCHAR(50) NOT NULL,
    ma_tai_san VARCHAR(50) NOT NULL,
    phan_loai_tai_san_id VARCHAR(50) NOT NULL,
    ten_ngoi_nha VARCHAR(500) NOT NULL,
    dia_chi VARCHAR(500),
    ma_px VARCHAR(5) NOT NULL,
    ten_px VARCHAR(256) NOT NULL,
    ma_qh VARCHAR(5) NOT NULL,
    ten_qh VARCHAR(256) NOT NULL,
    ma_tp VARCHAR(5) NOT NULL,
    ten_tp VARCHAR(256) NOT NULL,
    ds_file_dinh_kem TEXT,
    nguoi_tao VARCHAR(50),
    ngay_tao TIMESTAMPTZ NOT NULL,
    nguoi_sua VARCHAR(50),
    ngay_sua TIMESTAMPTZ,
    nguoi_xoa VARCHAR(50),
    ngay_xoa TIMESTAMPTZ,
    trang_thai_xoa BOOLEAN DEFAULT false,
	CONSTRAINT pbms_quan_ly_nha_cong_san_pk PRIMARY KEY (id)
);

GRANT REFERENCES, INSERT, UPDATE, TRUNCATE, TRIGGER, SELECT, DELETE ON TABLE qwc_config.pbms_quan_ly_nha_cong_san TO qwc_admin;

// 20241202: TODO
ALTER TABLE qwc_config.pbms_quan_ly_nhom_tham_so ADD COLUMN loai_ts VARCHAR(50);