  it('shows error message when fetch fails', async () => {
    axios.get.mockRejectedValueOnce(new Error('Network error'));
    await wrapper.vm.$nextTick();
-   expect(wrapper.text()).toContain('<placeholder_removed>');
+   expect(wrapper.text()).toContain('Unable to load review');
  });