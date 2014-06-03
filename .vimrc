"""" Piso-auction per-project .vimrc
set noexpandtab				" use tabs instead of spaces
set tabstop=4				" use 4 spaces for a tab
set shiftwidth=4			" set the default indentation width for smartindent
au BufNewFile,BufReadPost *.coffee setlocal ts=2 sts=2 sw=2 expandtab
au BufNewFile,BufReadPost *.python setlocal ts=4 sts=4 sw=4 noexpandtab
au BufNewFile,BufReadPost *.html setlocal ts=4 sts=4 sw=4 noexpandtab
"
""" macros
function! Cleanfile()
	if &modifiable
		" trim whitespace on save
		:%s/\s\+$//e
		:%s/	/\t/ge
	endif
endfunction
autocmd! bufreadpost *.python call Cleanfile()
autocmd! bufwritepre *.python call Cleanfile()
autocmd! bufreadpost *.html call Cleanfile()
autocmd! bufwritepre *.html call Cleanfile()

autocmd! bufwritepost *.coffee !batch/coffee-compile.sh
