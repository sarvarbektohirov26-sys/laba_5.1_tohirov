from main import main


def test_cli_ok(capsys):
    code = main(["--kind", "sine", "--n", "10", "--window", "3", "--seed", "1"])
    out = capsys.readouterr().out
    assert code == 0
    assert "SMA" in out and "EMA" in out


def test_cli_bad_n(capsys):
    code = main(["--n", "0"])
    err = capsys.readouterr().err
    assert code == 1
    assert "Ошибка" in err