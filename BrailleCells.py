import ctypes

class BrailleCells:
    functions = ctypes.CDLL("shared/libtest.so")
    MAX_OUTPUT_SIZE = 255

    @classmethod
    def braille_rep_size(cls, byte_array: bytes) -> int:
        """
        Tamaño de la representacion de un string en braille
        """
        return cls.functions.braille_rep_size(byte_array)

    @classmethod
    def valid_string(cls, string) -> bool:
        """
        valida si el string se puede convertir a braille

        El convertidor solo tiene soporte para caracteres
        ascii y tiene un limite maximo de 255 celdas braille.
        """

        try:
            bytes_str = bytes(string, 'ascii')
        except:
            print(f"El string '{string}' no se puede convertir a ascii")
            return False

        # 'functions.braille_rep_size' retorna el tamaño de la
        # represesentacion en braille mas el terminador
        if cls.braille_rep_size(bytes_str) > cls.MAX_OUTPUT_SIZE:
            print(
                f"la representacion del string '{string}' es mas grande que el tamaño del buffer de salida"
            )
            return False

        return True

    @classmethod
    def str_to_braille(cls, string_to_convert: str) -> list:
        """
        Convierte un string ascci a braille
        """

        if not cls.valid_string(string_to_convert):
            return list()

        output = []
        
        # https://stackoverflow.com/questions/61294630/ctypes-passing-a-string-as-a-pointer-from-python-to-c
        bytes_string = bytes(string_to_convert, 'ascii')
        ibuf = ctypes.create_string_buffer(bytes_string,
                                           size=cls.MAX_OUTPUT_SIZE)
        obuf = ctypes.create_string_buffer(b"", size=cls.MAX_OUTPUT_SIZE)

        cls.functions.str_to_braille(obuf, ibuf)

        for byte in obuf:
            foo = int.from_bytes(byte, "little")
            if foo != 0:
                output.append(foo)
            else:
                break

        return output
