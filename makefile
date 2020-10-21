BIN_DIR=$(PREFIX)/usr/bin
SYSTEMD_DIR=$(PREFIX)/usr/lib/systemd/system

install:
	cp src/three-finger-drag $(BIN_DIR)/three-finger-drag
	chmod 755 $(BIN_DIR)/three-finger-drag
	chown root:root $(BIN_DIR)/three-finger-drag || echo Chown failed, ignore

systemd_install:
	cp systemd/three-finger-drag.service $(SYSTEMD_DIR)/three-finger-drag.service
	chmod 644 $(SYSTEMD_DIR)/three-finger-drag.service
	chown root:root $(SYSTEMD_DIR)/three-finger-drag.service || echo Chown failed, ignore
