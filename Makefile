.PHONY: submodules fclean


submodules:
	git submodule update --recursive --rebase --remote --single-branch
	git submodule foreach git submodule update --init

fclean:
	rm -rf tg_bot checking login-logout notifier orioks_requester
