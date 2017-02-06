-- Adiciona permissão para que usuário "guest" do Postgres consiga ver as views

DROP OWNED BY guest;
DROP ROLE IF EXISTS guest;
CREATE ROLE guest;

GRANT guest to camaradeputados;
GRANT USAGE ON SCHEMA public TO guest;
GRANT SELECT ON votos TO guest;
GRANT SELECT ON presencas TO guest;
GRANT SELECT ON deputados TO guest;
