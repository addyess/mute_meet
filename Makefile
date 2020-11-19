EXTENSION=build/mute_meet.zip
EXT_SRC := extension
EXT_FILES := $(wildcard $(EXT_SRC)/*)

.PHONY: build
build: $(EXTENSION)

$(EXTENSION) : $(EXT_FILES)
	mkdir -p build/
	zip -r $(EXTENSION) $(EXT_SRC)
