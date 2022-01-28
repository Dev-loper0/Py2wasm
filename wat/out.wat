(module
	;;Here built in modules
	(import "console" "log" (func $PRINT (param i32)))
	(func (export "__start")
	(result ;;Here but return of main func
)
		;;to init vars
		(local $a i32)
		(local $b i32)

		;;Here start programm boy
		(local.set $a(i32.const 1))
		(local.set $b(i32.const 2))
		(local.get $a)
		(local.get $b)
		i32.lt_u
        (drop)
		(local.get $a)
		(call $PRINT)

		;;Here but the return

	)
)
