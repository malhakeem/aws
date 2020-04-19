--query 1
select user_id, count(*) from dwh.user_first_install_fact
WHERE datediff(day, installed_at, current_date) 
group by user_id
having count(*) > 1

--query 2
select ch.channel_name, count(*) from dwh.user_first_install_fact f
inner join dwh.channel_dim ch
on (f.channel_sk = ch.channel_sk)
inner join client_dim c
on (f.client_sk = c.client_sk)
where c.os_name ilike '%android%'
group by ch.channel_name
order by count(*) desc
limit 5
