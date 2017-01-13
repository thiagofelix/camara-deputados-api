-- Adiciona permissão para que usuário "guest" do Postgres consiga ver as views

DROP ROLE IF EXISTS guest;
DROP OWNED BY guest;
CREATE ROLE guest;

GRANT guest to camaradeputados;

GRANT USAGE ON SCHEMA public TO guest;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO guest;
