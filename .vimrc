"""" Piso-auction per-project .vimrc
set noexpandtab				" use tabs instead of spaces
set tabstop=4				" use 2 spaces for a tab
set shiftwidth=4			" set the default indentation width for smartindent
""" macros
function! Cleanfile()
	if &modifiable
		" convert spaces to tabs when reading and writing
		set noexpandtab
		retab! 4

		" trim whitespace on save
		:%s/\s\+$//e
	endif
endfunction
autocmd! bufreadpost * call Cleanfile()
autocmd! bufwritepre * call Cleanfile()
