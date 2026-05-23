TEST_FILES := $(wildcard test_*.py)

.PHONY: run-all $(TEST_FILES)

run-all: $(TEST_FILES)

# Rule to run a single test file
$(TEST_FILES):
	@echo "Tests in $@."
	-python -m unittest $@

run-unit:
	python -m unittest $(file)