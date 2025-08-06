async function page({
  params,
}: {
  params: Promise<{ id: string; billing_cycle: string }>;
}) {
  const { id, billing_cycle } = await params;

  return (
    <div>
      page - {id} - {billing_cycle}
    </div>
  );
}

export default page;
